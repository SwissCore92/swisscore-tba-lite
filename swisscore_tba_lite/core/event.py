import asyncio
import typing as t
import time
from datetime import timedelta
from inspect import iscoroutinefunction
from copy import deepcopy

from .logger import logger
from . import exceptions
from ..bot_api import literals

class UnhandledEventType: ...

EventName = literals.UpdateType | t.Literal["startup", "shutdown"]
HandlerFunction = t.Callable[[dict[str, t.Any], t.Any | None], t.Any | UnhandledEventType]
FilterFunction = t.Callable[[dict[str, t.Any]], bool]

TELEGRAM_EVENT_TYPES: frozenset[str] = frozenset(t.get_args(literals.UpdateType))

def func_info(f: t.Callable) -> str:
    return f"{f.__module__}.{f.__name__}@line={f.__code__.co_firstlineno}"

class EventManager:
    UNHANDLED = UnhandledEventType
    """
    Return this in an static event handler to mark the static event as unhandled and continue processing the update.  

    Return this in an temporary event handler to mark the temporary event as unhandled and continue processing on next matching update.  
    """
    
    def __init__(self, max_concurrent_handlers: int = 8):
        self.__startup_handler: EventHandler = None
        self.__shutdown_handler: EventHandler = None
        self.__temporary_handlers: dict[EventName, list[TemporaryEventHandler]] = {}
        self.__update_handlers: dict[EventName, list[EventHandler]] = {}
        self.__handler_control = asyncio.Semaphore(max_concurrent_handlers)
        self.__locked = False
        self.__tasks: list[asyncio.Task] = []
    
    def _lock(self):
        """*for internal use only*"""
        self.__locked = True

    def _get_handled_event_types(self) -> list[literals.UpdateType]:
        """
        Get a list of all currently handled event types.
        
        Is used for `allowed_updates`
        """
        return list(set([
            *self.__update_handlers.keys(), 
            *self.__temporary_handlers.keys()
        ]))
    
    def _remove_temporary_event_handler(self, tmp_event_handler: "TemporaryEventHandler", reason="handled"):
        """*for internal use only*"""
        self.__temporary_handlers[tmp_event_handler.type].remove(tmp_event_handler)
        if len(self.__temporary_handlers[tmp_event_handler.type]) == 0:
            self.__temporary_handlers.pop(tmp_event_handler.type)
        logger.debug(f"Removed {(repr(tmp_event_handler))} - Reason: {repr(reason)}")

    async def __process_update(self, event_name, obj, update_id) -> None:
        try:
            async with self.__handler_control:
                # check temporary handlers first
                if event_name in self.__temporary_handlers:
                    for tmp_handler in self.__temporary_handlers[event_name].copy():
                        
                        # TODO: check in realtime. not on matching update type
                        if tmp_handler.is_expired():
                            # remove expired event handler
                            self._remove_temporary_event_handler(tmp_handler, "expired")
                            continue

                        if await tmp_handler.matches(obj):
                            if handler := await tmp_handler.get_matching_handler(obj):
                                result = await handler(obj) if handler._arg_count == 1 else await handler(obj, tmp_handler.context)
                                if result is EventManager.UNHANDLED:
                                    # event handler returned that it is unhandled
                                    return True
                                else:
                                    # event handler returned nothing, so it is considered handled
                                    self._remove_temporary_event_handler(tmp_handler, "handled")
                                    return True
                            
                            logger.warning(f"{repr(tmp_handler)} matched. But none of its handlers did.")
                
                # check static handlers
                if handlers := self.__update_handlers.get(event_name):
                    for handler in handlers:
                        if await handler.matches(deepcopy(obj)):
                            if await handler(deepcopy(obj)) is EventManager.UNHANDLED:
                                logger.debug(f"{repr(handler)} returned EventManager.UNHANDLED! "
                                    "The event is considered unhandled. "
                                    "Continue checking for matching handlers."
                                )
                                continue
                                
                            return True

                logger.warning(f"No matching event handler found for update (ID={update_id}) of type '{event_name}'. Update was dropped.")
                return False
        
        except asyncio.CancelledError:
            pass
        
        except exceptions.RestartBotException as e:
            logger.debug("Restart flag set.")
            setattr(self, "restart_flag", True)
            
        except exceptions.FilterEvaluationError as e:
            logger.error(f"Failed to evaluate filters for update (ID={update_id}) of type '{event_name}'. Update was dropped. ({repr(e)})")
        
        except exceptions.EventHandlerError as e:
            logger.error(f"Failed to process update (ID={update_id}) of type '{event_name}'. Update was dropped. ({repr(e)})")

    async def _trigger_event(self, event_name: EventName, *args) -> None:
        """*for internal use only*"""
        match event_name:
            case "startup":
                if self.__startup_handler is not None:
                    await self.__startup_handler()
            
            case "shutdown":
                if self.__shutdown_handler is not None:
                    await self.__shutdown_handler(args[0])
            
            case _:
                obj: dict = args[0]
                update_id: int = args[1]

                # await self.__process_update(event_name, obj, update_id)

                task = asyncio.create_task(self.__process_update(event_name, obj, update_id), name=f"handle_update_{update_id}")
                self.__tasks.append(task)
                task.add_done_callback(self.__tasks.remove)

                
    def __call__(self, event_name: EventName, *filters: FilterFunction):
        """
        Resgister an event handler of any type.
        
        **Usage:**
        ```python
        # text messages
        @bot.event("message", is_text)
        async def on_text_message(msg):
            ...
        
        # photo messages with caption
        @bot.event("message", sub_keys("photo", "caption"))
        async def on_photo_message(msg):
            ...
        
        # every other unhandled message
        @bot.event("message")
        async def on_other_message(msg):
            ...
        ```
        
        **Note:**
        * Both Coroutine and regular functions are supported.
        * A filter **must match** the signature `func(obj: dict)` where `obj` is *always* a `dict`!
        * A filter is satisfied if `bool(your_filter(obj)) == True`
        * The filters are checked in order. 
        * Event handlers are checked in the order you defined them from top to bottom.
        * Event handlers without filters should always be defined **at the bottom** of all other handlers of **the same type** (`event_name`).

        Args:
            event_name (str): The name of the event.  
            filters (list[Callable], optional): A list of filter functions.  
        """

        if self.__locked:
            raise RuntimeError("It's not allowed to register static event handlers at runtime.")

        def register(func: t.Callable[[dict], t.Any]):
            exceptions.raise_for_not_coro(func)
            
            match event_name:
                case "startup":
                    if filters:
                        raise TypeError("'startup' event handler takes no filters.")
                    exceptions.raise_for_non_matching_arg_count(func, 0)
                    if self.__startup_handler is not None:
                        raise TypeError("There can only be one 'startup' event handler.")
                    self.__startup_handler = EventHandler("startup", func)
                    
                case "shutdown":
                    if filters:
                        raise TypeError("'shutdown' event handler takes no filters.")
                    exceptions.raise_for_non_matching_arg_count(func, 1)
                    if self.__shutdown_handler is not None:
                        raise TypeError("There can only be one 'shutdown' event handler.")
                    self.__shutdown_handler = EventHandler("shutdown", func)
                
                case _:
                    if event_name not in TELEGRAM_EVENT_TYPES:
                        raise KeyError(f"'{event_name}' is an invalid event_name")

                    if func.__code__.co_argcount == 2:
                        # this event handler is likely used as temporary handler
                        if not func.__defaults__:
                            raise TypeError(f"The second argument of {func_info(func)} `{func.__code__.co_varnames[1]}` must have a default value.")
                    elif func.__code__.co_argcount != 1:
                        raise TypeError(f"The event handler {func_info(func)} must accept exactly 1 or 2 arguments.")
                    
                    if not event_name in self.__update_handlers:
                        self.__update_handlers[event_name] = []

                    handler = EventHandler(event_name, func, list(filters))

                    for previous_handler in reversed(self.__update_handlers[event_name]):
                        # TODO: Check if UNHANDLED is returned
                        if not previous_handler.filters:
                            logger.warning(
                                f"{repr(handler)} may never be triggered because "
                                f"{repr(previous_handler)} has no filters and is defined above it."
                            )
                    
                    self.__update_handlers[event_name].append(handler)

            return func
        
        return register
    
    def wait_for(
        self, 
        event_name: EventName, 
        *filters: FilterFunction,
        handlers: list[tuple[HandlerFunction, list[FilterFunction]]], 
        context: t.Any | None = None,
        timeout: float | timedelta | None = None
    ) -> None:
        """
        create a temporary event listener.

        Args:
            event_name: name of the event
            handlers: the temporary handlers
            context (optional): an optional context (can be anything)
            shared_filters (optional): a list of shared filters. **Note:** these are checked first.
            timeout (optional): a timeout for the temporary handler (in seconds).  

        Example usage:
        ```python
        # add a test command handler
        @bot.event("message", chat_types("private"), commands("test"))
        async def test_cmd(msg: dict):
            # define a temporary handler
            async def countdown(m: dict, ctx: dict):
                if ctx["count"] > 0:
                    bot("sendMessage", {
                        "chat_id": m["chat"]["id"],
                        "text": f"Explode after {ctx["count"]}..."
                    })
                    ctx["count"] -= 1
                    return bot.event.UNHANDLED
                
                bot("sendMessage", {
                    "chat_id": msg["chat"]["id"],
                    "text": "BOOM! 💥"
                })
            
            context = {"count": 3}
            await countdown(msg, context)

            # register the temporary handler
            bot.event.wait_for("message", [
                (countdown, [chat_ids(msg["chat"]["id"])]),
            ], context=context)
        ```

        """
        if event_name not in TELEGRAM_EVENT_TYPES:
            raise KeyError(f"'{event_name}' is an invalid event_name")
        
        if event_name not in self._get_handled_event_types():
            # TODO: update allowed_updates instead
            logger.warning(f"'{event_name}' is not in 'allowed_updates'")
            return

        expires_at = None
        if isinstance(timeout, timedelta):
            timeout = timeout.seconds
        if isinstance(timeout, (int, float)):
            expires_at = time.time() + timeout
        
        handler = TemporaryEventHandler(
            event_name, 
            [EventHandler(event_name, handler, filters) for handler, filters in handlers], 
            context=context, 
            filters=list(filters),
            expires_at=expires_at
        )

        if not event_name in self.__temporary_handlers:
            self.__temporary_handlers[event_name] = []
        self.__temporary_handlers[event_name].append(handler)
        logger.debug(f"Added {(repr(handler))}")


class EventHandler:
    def __init__(
        self, 
        type: EventName, 
        func: HandlerFunction, 
        filters: list[FilterFunction] | None = None
    ) -> None:
        self.type = type
        self.func = func
        self.filters = filters
        self._arg_count = func.__code__.co_argcount
        
        if self.filters:
            for f in filters:
                exceptions.raise_for_non_matching_arg_count(f, 1)
        
        self.__name__ = func.__name__
    
    def __str__(self):
        return self.__name__
    
    def __repr__(self):
        return f"{self.__class__.__name__}(type='{self.type}', func={func_info(self.func)})"
    
    async def __call__(self, *args, **kwargs) -> t.Awaitable[t.Any | UnhandledEventType]:
        try:
            logger.debug(f"Running {repr(self)}")
            return await self.func(*args, **kwargs)

        except exceptions.RestartBotException as e:
            raise

        except Exception as e:
            logger.error(f"Exception in {repr(self)}: {e}", exc_info=True)
            raise exceptions.EventHandlerError(
                f"Error in '{self.type}' event handler {self.__name__}. Error: {repr(e)}"
            ) from e
    
    async def matches(self, update_obj: dict[str, t.Any]) -> bool:
        try:
            if self.filters:
                return all([
                    await f(update_obj) if iscoroutinefunction(f) else f(update_obj) for f in self.filters
                ])
            return True
        
        except Exception as e:
            logger.error(f"Exception while evaluating {repr(self)}: {repr(e)}", exc_info=True)
            raise exceptions.FilterEvaluationError(
                f"Error in {repr(self)} filter evaluation. Error: {e}"
            ) from e

class TemporaryEventHandler:
    def __init__(
        self, 
        type: str, 
        handlers: list[EventHandler], 
        context: t.Any | None = None, 
        filters: list[FilterFunction] | None = None,
        expires_at: float | None = None
    ):
        self.type = type

        for h in handlers:
            if h._arg_count > 2:
                raise TypeError(f"The temporary event handler {func_info(h.func)} must accept exactly 1 or 2 arguments.")

        self.handlers = handlers
        self.context = context
        self.filters = filters
        self.expires_at = expires_at
    
    def is_expired(self) -> bool:
        if self.expires_at == None:
            return False
        return time.time() > self.expires_at
    
    async def matches(self, update_obj: dict[str, t.Any]) -> bool:
        if not self.filters:
            return True
        try:
            return all([
                await f(update_obj) if iscoroutinefunction(f) else f(update_obj) for f in self.filters
            ])
        
        except Exception as e:
            logger.error(f"Exception while evaluating {repr(self)}: {repr(e)}", exc_info=True)
            raise exceptions.FilterEvaluationError(
                f"Error in {repr(self)} filter evaluation. Error: {e}"
            ) from e

    async def get_matching_handler(self, update_obj: dict[str, t.Any]) -> EventHandler | None:
        for handler in self.handlers:
            if await handler.matches(update_obj):
                return handler
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.type=})"
    
    def __repr__(self):
        handlers = [func_info(h.func) for h in self.handlers]
        return f"{self.__class__.__name__}(type={self.type}, context={self.context}, handlers={handlers})"
