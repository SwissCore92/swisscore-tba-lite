import asyncio
import typing as t
from functools import wraps
 
import aiohttp

from .. import utils
from .logger import logger
from .event import EventManager
from .exit_codes import ExitCodes
from . import exceptions

T = t.TypeVar("T")

# decorator
def request_task_wrapper(catch_errors: bool):
    """
    *decorator* for the request task coroutine.
    
    **Is used internally**
    """
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            
            # TODO: Maybe use custom exception for uninitialized session  
            except RuntimeError as e:
                logger.critical(e, exc_info=True)
                # Always raise this exception
                raise

            except (
                exceptions.FileProcessingError, 
                exceptions.InvalidParamsError,
                exceptions.ResultConversionError
            ) as e:
                # mostly user caused error 
                logger.error(e, exc_info=True)
                
                if not catch_errors:
                    raise
            
            except (exceptions.TelegramAPIError) as e:
                if e.critical:
                    logger.critical(e)
                     
                    if isinstance(e, exceptions.Conflict):
                        logger.warning(
                            "If this conflict wasn't caused by you, it means that somebody else may have access to your API_TOKEN. "
                            "Consider to revoke your API_TOKEN via @BotFather in this case!"
                        )
                        
                else:
                    logger.error(e)
                
                if not catch_errors:
                    raise
            
            except exceptions.MaxRetriesExeededError as e:
                logger.error(e)
                
                if not catch_errors:
                    raise
            
            except Exception as e:
                logger.critical(e, exc_info=True)
                
                if not catch_errors:
                    raise
                
        return inner
    
    return wrapper
        
# decorator
def api_method_wrapper(
    name: str | None = None,
    *,
    check_input_files: list[str] | None = None,
    check_input_media: list[str] | None = None,
    convert_func: t.Callable[[t.Any], t.Any] | None = None,
):
    """
    **decorator** for api methods
    
    ⚠️ ***Can only be applied to methods of `BaseBot` or is's subclasses***
    
    It's purpose is to make it very easy to extend the `BaseBot` class.
    
    **Ussage:**
    ```python
    
    class Bot(BaseBot):
        @api_method_wrapper()
        def send_message(self, chat_id, text, ...):
            \"""No Code needed, the decorator handles the request\"""
        
        @api_method_wrapper(check_input_files=["photo"])
        def send_photo(self, chat_id, photo, ...):
            \"""No Code needed, the decorator handles the request\"""
        
        ...
    ```
    """
    
    def wrapper(func):
        
        method_name = name or utils.snake_to_camel(func.__name__)

        def inner(*args, **kwargs):
            params = dict(zip(func.__code__.co_varnames, args))
            params.update(kwargs)
            
            bot: BaseBot = params.pop("self")
            
            if not isinstance(bot, BaseBot):
                raise TypeError(f"This decorator can only be applied to instances of BaseBot.")
            
            return bot(
                method_name, 
                params=params,
                check_input_files=check_input_files,
                check_input_media=check_input_media,
                convert_func=convert_func,
            )
            
        return inner
    
    return wrapper

# helper function
async def prepare_files(
    params: dict[str, t.Any], 
    check_input_files: list[str] | None = None, 
    check_input_media: list[str] | None = None,
) -> tuple[dict[str, t.Any] | None, aiohttp.FormData | None]:
    form_data: aiohttp.FormData | None = None
    
    check_input_files = check_input_files or []
    check_input_media = check_input_media or []
    
    if check_input_files or check_input_media:
        try:
            input_files = await utils.process_input_files(params, check_input_files)
            media_files, input_media = await utils.process_input_media(params, check_input_media)
            input_files.update(media_files) 

            if input_files:
                form_data = await utils.create_form_data(params, input_files)
        
        except FileNotFoundError as e:
            raise exceptions.FileProcessingError(
                f"Provided file was not found."
            ) from e
        
        except IOError as e:
            raise exceptions.FileProcessingError(
                f"Error occured while reading file."
            ) from e
        
        except Exception as e:
            raise exceptions.FileProcessingError(
                f"A unexcepted error occured while preparing files."
            ) from e

    if form_data is not None:
        return None, form_data
    
    return params, None

# helper function
def serialize_params(params: dict[str]) -> dict[str]:
    try:
        params = {
            k: utils.dumps(v) if isinstance(v, (dict, list, tuple)) else v
            for k, v in params.items() 
            if v is not None
        }
    except TypeError as e:
        raise exceptions.InvalidParamsError(
            f"Exception while preparing params. "
            "Did you forgot to set 'check_input_files' / 'check_input_media'? {e}"
        ) from e


class BaseBot:
    """
    ## The Base Telegram Bot.  
    
    * Only core functionality
    * Requests must be made using `bot("<method_name>", {<params>})`
    * Handles only in dicts
    """
    def __init__(
        self, 
        token: str, 
        *, 
        base_api_url: str = "https://api.telegram.org",
        base_file_url: str = "https://api.telegram.org/file",
        event_manager: EventManager | None = None
    ) -> None:
        
        # Checking for valid bot api token
        if not utils.is_valid_bot_api_token(token):
            raise TypeError(f"'{token}' is not a valid Telegram Bot API Token!")
        
        self.event = event_manager or EventManager()
        """
        The event manager.
        
        Use this decorator to register events
        """
        
        self.api_url = f"{base_api_url}/bot{token}"
        """
        The API url in the format `https://api.telegram.org/bot<token>`.  
        
        **Is internally used to make api requests.**
        """
        
        self.file_url = f"{base_file_url}/bot{token}"
        """
        The file url in the format `https://api.telegram.org/file/bot<token>`.  
        
        **Is internally used to download files.**
        """
        
        self.session: aiohttp.ClientSession | None = None
        """
        The client session is initialized when the bot is started.  
        
        You can savely use this to make your own requests.
        """
        
        self.polling_timeout: int = 20
        """
        Timeout in seconds for long polling.    
        
        Should be positive, short polling (a timeout of 0) should be used for testing purposes only.
        """
        
        self.update_limit: int | None = None
        """
        Limits the number of updates to be retrieved per polling cycle.  
        
        Values between 1-100 are accepted. Defaults to `None` which means 100.
        """
        
        self.log_successful_requests: bool = False
        """
        If set to `True`, a DEBUG message is logged on a successful request.
        """
        
        self.max_retries: int = 5
        """
        Max retries for transient request errors (`TooManyRequests`, `TimeoutError`, etc.).
        """
        
        # # Not used at the moment. currently using `max_retries` for connection errors
        # self.max_connection_retries: int = 10
        # """
        # Max retries for connection errors.
        # """
        
        self.default_timeout: int = 30
        """
        Default timeout to use if not provided.
        """
        
        self.max_timeout: int = 60
        """
        Limits the max timeout for retrying timed out requests.
        """
        
        self.max_concurrent_tasks: int = 50
        """
        Max amount of concurrent tasks.  
        If the limit is exceeded, the bot will automatically gather all pending tasks before it continues processing updates.
        """
        
        self._tasks: list[asyncio.Task] = []
        """
        Stores currently running tasks to protect them from beeing collected by the garbage collector.  
        
        **Is used internally to manage tasks**
        """

    
    def _create_task(self, coro, name=None) -> asyncio.Task:
        """
        Create a new task.  
        
        **For internal use**
        """
        task = asyncio.create_task(coro, name=name)
        self._tasks.append(task)
        task.add_done_callback(self._tasks.remove)
        return task
    
    
    async def _gather_pending_tasks(self):
        """
        Wait for the completion of all spawned tasks.  
        
        **For internal use**
        """
        if self._tasks:
            # TODO: Maybe catch errors here. Bot can crash if an unawaited pending task raises an error outside an event handler
            logger.debug(f"Waiting for {len(self._tasks)} pending task(s) to complete: {[tsk.get_name() for tsk in self._tasks]}")
            await asyncio.gather(*self._tasks)
        logger.debug("All pending tasks completed")
    
    
    def start_polling(self) -> None:
        """
        Start the bot in [long polling](https://en.wikipedia.org/wiki/Push_technology#Long_polling) mode.  
        
        Uses the [`getUpdates`](https://core.telegram.org/bots/api#getupdates) API method to get [Updates](https://core.telegram.org/bots/api#update).  
        
        **Note:**
        * *`offset`* is calculated automatically
        * *`limit`* can be set using `bot.update_limit = <limit>` (defaults to `None` which is 100)
        * *`timeout`* can be set using `bot.polling_timeout = <timeout>` (defaults to 20)
        * *`allowed_updates`* are automatically set, based on your event handlers
        
        Is just a shortcut for
        ```python
        asyncio.run(bot._polling_main_loop())
        ```
        
        """
        logger.debug("Start async event loop")
        
        asyncio.run(self._polling_main_loop())
        
        logger.debug("Closed async event loop")
    
    
    async def _polling_main_loop(self) -> None:
        """
        Iterates over incoming updates and triggers the matching event handlers.  
        
        To start polling use 
        ```python
        bot.start_polling()
        ```
        > *or*
        ```python
        asyncio.run(bot._polling_main_loop())
        ```
        """
        async for update in self._get_future_updates():
            try:
                update_id = update["update_id"]
                update_type = utils.get_update_type(update)
                update_object = update[update_type]
                
                await self.event._trigger_event(update_type, update_object)
                
                if len(self._tasks) >= self.max_concurrent_tasks:
                    logger.info(
                        f"Max amount of concurrent tasks exceeded ({self.max_concurrent_tasks}). "
                        "Gathering all pending tasks before processing further updates..."
                    )
                    await self._gather_pending_tasks()
            
            except exceptions.FilterEvaluationError as e:
                logger.error(f"Failed to process update of type '{update_type}'. Update was dropped. ({e})", exc_info=True)
            
            except exceptions.EventHandlerError as e:
                logger.error(f"A event handler processing an update of type '{update_type}' crashed. ({e})", exc_info=True)
    
    
    async def _get_future_updates(
        self,
        drop_pending_updates: bool = False
    ) -> t.AsyncGenerator[dict[str, t.Any], None]:
        """
        Generator that asks repeatedly for new updates and yields them one by one.  
        
        **Is used internally**
        """
        exit_code: int = 0
        
        params = {
            "offset": 0, 
            "limit": self.update_limit, 
            "timeout": self.polling_timeout,
            "allowed_updates": self.event._get_handled_event_types()
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        logger.debug("Start client session")
        
        async with aiohttp.ClientSession() as session:
            self.session = session

            if drop_pending_updates:
                if updates := await self.__call__("getUpdates", params={"offset": -1}, auto_prepare=False):
                    logger.debug("Dropped pending updates.")
                    params["offset"] = updates[-1]["update_id"] + 1
            
            try:
                await self.event._trigger_event("startup")
                await self._gather_pending_tasks()
                
            except (exceptions.FilterEvaluationError, exceptions.EventHandlerError) as e:
                logger.error(f"Error in 'startup' event handler. ({e})", exc_info=True)
            
            logger.info(f"Start Bot in long polling mode. Press {utils.kb_interrupt()} to quit.")
            
            while True:
                try: 
                    if updates := await self.__call__("getUpdates", params=params, auto_prepare=False, catch_errors=False):
                        logger.debug(f"Received {len(updates)} new update(s).")
                        for update in updates:
                            yield update
                    
                        params["offset"] = updates[-1]["update_id"] + 1

                except exceptions.MaxRetriesExeededError as e:
                    logger.error(f"Failed to get updates. Check your Internet Connection. Retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                
                except asyncio.exceptions.CancelledError:
                    exit_code = ExitCodes.TERMITATED_BY_USER
                    logger.info(f"{utils.kb_interrupt()} pressed. Shutting down with {exit_code=}.")
                    break
                
                except exceptions.TelegramAPIError as e:
                    if e.critical:
                        # Only happens when '409: Conflict' or '403: Forbidden' is raised
                        exit_code = ExitCodes.CRITICAL_TELEGRAM_ERROR
                        logger.critical(f"Shutting down with {exit_code=}.")
                            
                    else:
                        # Should not happen in theory. (The getUpdate request was invalid, logging with exc_info)
                        logger.critical(f"Failed to get updates due an unexpected Telegram API Error. {repr(e)}", exc_info=True)
                        exit_code = ExitCodes.UNEXPECTED_TELEGRAM_ERROR
                        
                    break
                
                except Exception as e:
                    exit_code = ExitCodes.UNEXPECTED_ERROR
                    logger.critical(f"A critical, unexpected error occured. Shutting down with {exit_code=}.", exc_info=True)
                    break
            
            try:
                await self.event._trigger_event("shutdown", exit_code)
                await self._gather_pending_tasks()
            
            except (exceptions.FilterEvaluationError, exceptions.EventHandlerError) as e:
                logger.error(f"Error in 'shutdown' event handler. ({e})", exc_info=True)

        self.session = None
        logger.debug("Closed client session")


    def __call__(
        self, 
        method_name: str, 
        params: dict[str] | None = None,
        *,
        auto_prepare: bool = True,
        check_input_files: list[str] | None = None, 
        check_input_media: list[str] | None = None,
        timeout: int | None = None,
        convert_func: t.Callable[[t.Any], T] | None = None,
        catch_errors: bool = True,
    ) -> asyncio.Task[dict[str] | T]:
        """
        Use this method to make [API](https://core.telegram.org/bots/api) requests.

        **Ussage:**
        ```python
        bot("sendMessage", {"chat_id": chat_id, "text": "Hello world!"})
        me = await bot("getMe") 
        ```

        Returns a asyncio.Task which can be awaited to get the result.
        
        > ⚠️ ***Warning:***  
        > * *Using this method when the bot isn't yet started will raise a `RuntimeError` even if `catch_errors` is set to `True`! Use the 'startup' event if you need to make requests on startup!*  
        > * *If you set `catch_errors` to `False` **you must await the Task**! If you don't, the bot **may crash** if an Error occures!* 
        
        """
        
        if self.session is None:
            # TODO: Maybe use custom exception for uninitialized session  
            raise RuntimeError("Client session is not initialized.")
        
        timeout = timeout or self.default_timeout

        @request_task_wrapper(catch_errors=catch_errors)
        async def request():
            nonlocal params
            nonlocal timeout

            data: aiohttp.FormData | None = None
            if params and (check_input_files or check_input_media):
                # may raise a FileProcessingError
                params, data = await prepare_files(params, check_input_files, check_input_media)
                    
            if auto_prepare and params:
                # may raise an InvalidParamsError
                serialize_params(params)

            url = f"{self.api_url}/{method_name}"
            
            retries = 0

            while retries < self.max_retries:
                
                timeout = min(timeout, self.max_timeout)
            
                try:
                    async with self.session.post(
                        url, 
                        params=params, 
                        data=data, 
                        timeout=timeout,
                    ) as r:
                        
                        await exceptions.raise_for_telegram_error(method_name, r)
                        
                        response: dict[str] = await r.json()

                        if self.log_successful_requests:
                            logger.debug(f"'{method_name}' -> HTTP {r.status}: OK")
                        
                        result = response["result"]
                        
                        if callable(convert_func):
                            try:
                                result = convert_func(result)
                            
                            except Exception as e:
                                raise exceptions.ResultConversionError(
                                    f"Error in '{convert_func.__name__}'. Conversion of result failed: {e}"
                                ) from e
                        else:
                            return result 
                
                except exceptions.FileProcessingError as e:
                    raise
                
                except exceptions.InvalidParamsError as e:
                    raise
                
                except exceptions.TelegramAPIError as e:
                    if e.retryable and e.retry_after:
                        logger.warning(f"'{method_name}' -> {e} - Retrying after {e.retry_after} seconds...")
                        await asyncio.sleep(e.retry_after)
                        retries += 1
                        continue
                    
                    e.message = f"'{method_name}' -> {e.message}"
                    raise
                
                except asyncio.TimeoutError as e:
                    wait_time = 2**retries
                    logger.warning(f"'{method_name}' timed out. - Retrying after {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    timeout += 10
                    retries += 1
                    continue
                
                except aiohttp.ClientOSError as e:
                    wait_time = 2**retries
                    logger.warning(f"'{method_name}' Network issue detected. Check your internet connection. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    timeout += 10
                    retries += 1
                    continue
                
                except Exception as e:
                    # Unexpected Error. raise.  
                    raise
            
            raise exceptions.MaxRetriesExeededError(f"'{method_name}' Max retries exceeded. Request failed.")
        
        return self._create_task(request(), name=method_name)
    
