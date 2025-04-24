import typing as t
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
    Return this in an event handler to mark the event as unhandled and continue processing the update.  
    
    This allows you to make small, single purpose handlers without filter spaghetti.
    
    Usage:
    ```python
    
    from swisscore_tba_lite.filters import sub_keys
    
    @bot.event("message", sub_keys("document", "mime_type")):
    async def handle_pdf(msg):
        if msg["document"]["mime_type"] != "application/pdf":
            return bot.event.UNHANDLED
        
        # Handle pdf document
    
    @bot.event("message", sub_keys("document", "mime_type")):
    async def handle_file(msg):
        ...
        # Continue handling the document (which is no pdf file)
    ```
    """
    
    def __init__(self):
        self.__startup_handler: EventHandler = None
        self.__shutdown_handler: EventHandler = None
        self.__temporary_handlers: dict[EventName, list[TemporaryEventHandler]] = {}
        self.__update_handlers: dict[EventName, list[EventHandler]] = dict((k, []) for k in TELEGRAM_EVENT_TYPES)
    
    def _get_handled_event_types(self) -> list[str]:
        """
        Get a list of all handled event types.
        
        Is used for `allowed_updates`
        """
        return [k for k, v in self.__update_handlers.items() if v]
    
    async def _trigger_event(self, event_name: EventName, *args) -> bool:
        match event_name:
            case "startup":
                if self.__startup_handler is not None:
                    await self.__startup_handler()
                    return True
            
            case "shutdown":
                if self.__shutdown_handler is not None:
                    await self.__shutdown_handler(args[0])
                    return True
            
            case _:
                obj: dict = args[0]

                # check temporary handlers first
                if event_name in self.__temporary_handlers:
                    hanlded_tmp_event: TemporaryEventHandler | None = None
                    for tmp_handler in self.__temporary_handlers[event_name]:
                        if handler := await tmp_handler.matches(obj):
                            result = await handler(obj) if handler._arg_count == 1 else await handler(obj, tmp_handler.context)
                            if result is EventManager.UNHANDLED:
                                # event handler returned that it is unhandled
                                return
                            else:
                                # event handler returned nothing, so it is considered handled
                                hanlded_tmp_event = tmp_handler
                            break
                    if hanlded_tmp_event:
                        # remove temporay event
                        self.__temporary_handlers[event_name].remove(hanlded_tmp_event)
                        logger.debug(f"Removed {(repr(hanlded_tmp_event))}")
                        if len(self.__temporary_handlers[event_name]) == 0:
                            self.__temporary_handlers.pop(event_name)
                        return

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

                logger.warning(f"No matching event handler found for update of type '{event_name}'. Update was dropped.")
                return False
                

    def __call__(self, event_name: EventName, *filters: t.Callable[[dict[str, t.Any]], t.Any]):
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
        
        `event_name` must be one of:  
        * "startup" (*Triggered on startup right after the client session is started but before updates are received*)
        * "shutdown" (*Triggered on shutdown right after receiving updates but before the client session is closed*)
        * "message" (*Triggered when a update of type "message" is received*)
        * "edited_message" (*Triggered when a update of type "edited_message" is received*)
        * "channel_post" (*Triggered when a update of type "channel_post" is received*)
        * "edited_channel_post" (*Triggered when a update of type "edited_channel_post" is received*)
        * "business_connection" (*Triggered when a update of type "business_connection" is received*)
        * "business_message" (*Triggered when a update of type "business_message" is received*)
        * "edited_business_message" (*Triggered when a update of type "edited_business_message" is received*)
        * "deleted_business_messages" (*Triggered when a update of type "deleted_business_messages" is received*)
        * "message_reaction" (*Triggered when a update of type "message_reaction" is received*)
        * "message_reaction_count" (*Triggered when a update of type "message_reaction_count" is received*)
        * "inline_query" (*Triggered when a update of type "inline_query" is received*)
        * "chosen_inline_result" (*Triggered when a update of type "chosen_inline_result" is received*)
        * "callback_query" (*Triggered when a update of type "callback_query" is received*)
        * "shipping_query" (*Triggered when a update of type "shipping_query" is received*)
        * "pre_checkout_query" (*Triggered when a update of type "pre_checkout_query" is received*)
        * "purchased_paid_media" (*Triggered when a update of type "purchased_paid_media" is received*)
        * "poll" (*Triggered when a update of type "poll" is received*)
        * "poll_answer" (*Triggered when a update of type "poll_answer" is received*)
        * "my_chat_member" (*Triggered when a update of type "my_chat_member" is received*)
        * "chat_member" (*Triggered when a update of type "chat_member" is received*)
        * "chat_join_request" (*Triggered when a update of type "chat_join_request" is received*)
        * "chat_boost" (*Triggered when a update of type "chat_boost" is received*)
        * "removed_chat_boost" (*Triggered when a update of type "removed_chat_boost" is received*)
        
        **Note:**
        * Both Coroutine and regular functions are supported.
        * A filter **must match** the signature `func(obj: dict)` where `obj` is *always* a `dict`!
        * A filter is satisfied if `bool(your_filter(obj)) == True`
        * The filters are checked in order. 
        * Event handlers are checked in the order you defined them from top to bottom.
        * Event handlers without filters should always be defined at the bottom of all other handlers of the same type (`event_name`).

        Args:
            event_name (str): The name of the event.  
            filters (list[Callable], optional): A list of filter functions.  
        """

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
                        # this event handler is likely used as tmp handler too
                        if not func.__defaults__:
                            raise TypeError(f"The second argument of {func_info(func)} `{func.__code__.co_varnames[1]}` must have a default value.")
                    elif func.__code__.co_argcount != 1:
                        raise TypeError(f"The event handler {func_info(func)} must accept exactly 1 or 2 arguments.")

                    handler = EventHandler(event_name, func, list(filters))

                    for previous_handler in reversed(self.__update_handlers[event_name]):
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
        handlers: list[tuple[HandlerFunction, list[FilterFunction]]], 
        *,
        context: t.Any | None = None,
        shared_filters: list[FilterFunction]
    ) -> None:
        """
        create a temporary event listener.

        Args:
            event_name: name of the event
            handlers: the temporary handlers
            context (optional): an optional context (can be anything)
            shared_filters (optional): a list of shared filters. **Note:** these are checked first.

        Example usage:
        ```python
        # add a test command handler
        @bot.event("message", chat_types("private"), commands("test"))
        async def test_cmd(msg: tg.Message):
            # define a temporary handler
            async def countdown(m: tg.Message, ctx):
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
            
            bot("sendMessage", {
                "chat_id": msg["chat"]["id"],
                "text": "Explode after 3..."
            })

            # register the temporary handler
            bot.event.wait_for("message", [
                (countdown, [chat_ids(msg["chat"]["id"])]),
            ], context={"count": 2})
        ```

        """
        if event_name not in TELEGRAM_EVENT_TYPES:
            raise KeyError(f"'{event_name}' is an invalid event_name")
        
        if not event_name in self.__temporary_handlers:
            self.__temporary_handlers[event_name] = []
        
        if not shared_filters:
            shared_filters = []
        
        handler = TemporaryEventHandler(
            event_name, 
            [EventHandler(event_name, x[0], [*shared_filters, *[1]]) for x in handlers], 
            context=context, 
            shared_filters=shared_filters
        )
        self.__temporary_handlers[event_name].append(handler)
        logger.debug(f"Added {(repr(handler))}")


class EventHandler:
    def __init__(
        self, 
        type: EventName, 
        func: t.Callable[[dict[str, t.Any]], None | UnhandledEventType], 
        filters: list[t.Callable[[dict[str, t.Any]], bool]] | None = None
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
            logger.error(f"Exception while evaluating {self}: {repr(e)}", exc_info=True)
            raise exceptions.FilterEvaluationError(
                f"Error in {repr(self)} filter evaluation. Error: {e}"
            ) from e

class TemporaryEventHandler:
    def __init__(self, type: str, handlers: list[EventHandler], context: t.Any | None = None):
        self.type = type

        for h in handlers:
            if h._arg_count > 2:
                raise TypeError(f"The temporary event handler {func_info(h.func)} must accept exactly 1 or 2 arguments.")

        self.handlers = handlers
        self.context = context

    async def matches(self, update_obj: dict[str, t.Any]) -> EventHandler | None:
        for i, handler in enumerate(self.handlers):
            if await handler.matches(update_obj):
                return handler
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.type=})"
    
    def __repr__(self):
        handlers = [func_info(h.func) for h in self.handlers]
        return f"{self.__class__.__name__}(type={self.type}, context={self.context}, handlers={handlers})"
