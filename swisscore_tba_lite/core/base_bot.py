import asyncio
import typing as t
import subprocess
import sys
from functools import wraps

import httpx

from .. import utils
from ..utils.files import prepare_files
from .logger import logger
from .event import EventManager
from . import exit_codes
from . import exceptions
from ..utils.file_downloader import FileDownloader
from ..bot_api import literals
from ..bot_api import objects

T = t.TypeVar("T")
JsonDict = dict[str, t.Any]

CLOUD_BOT_API_URL = "https://api.telegram.org"
CLOUD_BOT_FILE_URL = "https://api.telegram.org/file"

USE_CLOUD_URL = frozenset({"logout"})
"""
methods that always must be dispatched to the cloud telegram bot api server
"""

# decorator
def request_task_wrapper(catch_errors: bool, rate_control: asyncio.Semaphore):
    """
    *decorator* for the request task coroutine.
    
    **Is used internally**
    """
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            try:
                async with rate_control:
                    return await func(*args, **kwargs)
            
            # TODO: Maybe use custom exception for uninitialized client  
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
    
    **Usage:**
    ```python

    class Message:
        def __init__(self, message_id, ...):
            ...
    
    class Bot(BaseBot):
        @api_method_wrapper(convert_func=lambda d: Message(**d))
        def send_message(self, chat_id: int | str, text: str, ...):
            \"""
            Just add the doc sting.  
            No Code needed, the decorator handles the request
            \"""
        
        @api_method_wrapper(check_input_files=["photo"], convert_func=lambda d: Message(**d))
        def send_photo(self, chat_id: int | str, photo: str | Path | bytes, ...):
            \"""
            Just add the doc sting.  
            No Code needed, the decorator handles the request
            \"""
        
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
def serialize_params(params: JsonDict) -> JsonDict:
    try:
        params = {
            k: utils.dumps(v) if isinstance(v, (dict, list, tuple)) else v
            for k, v in params.items() 
            if v is not None
        }
        return params
    except TypeError as e:
        raise exceptions.InvalidParamsError(
            f"Exception while preparing params. "
            "Did you forgot to set 'check_input_files' / 'check_input_media'? {e}"
        ) from e

# core function, but no need to expose
async def run_builtin_event(bot: "BaseBot", event_name: str, *args):
    try:
        await bot.event._trigger_event(event_name, *args)
        await bot._gather_pending_tasks()
    
    except exceptions.RestartBotException:
        logger.error(f"RestartBotExcepiton not allowed in '{event_name}' event handler!")
    
    except (exceptions.FilterEvaluationError, exceptions.EventHandlerError) as e:
        logger.error(f"Error in '{event_name}' event handler. ({e})", exc_info=True)

class BaseBot:
    """
    ## The Base Telegram Bot.  
    
    * Focus on core functionality amd expandability
    * Requests must be made using `bot("<method_name>", {<params>})`
    * Handles only in dicts
    """
    def __init__(
        self, 
        token: str, 
        *, 
        base_api_url: str = CLOUD_BOT_API_URL,
        base_file_url: str = CLOUD_BOT_FILE_URL,
        event_manager: EventManager | None = None,
        max_concurrent_requests: int = 50
    ) -> None:
        """
        Initialize your bot.  
        
        Args:
            token (str): The token you received from @BotFather
            base_api_url (str, optional): The base url for api calls; **Only change this if you're using your own Telegram Bot API**.  
            base_file_url (str, opional): The base url for files to download; **Only change this if you're using your own Telegram Bot API**. 
            event_manager (EventManager, optional): The `EventManager` to use; **Only set this if you are expanding the bot and need a more advanced event manager.**
        """
        
        if not utils.is_valid_bot_api_token(token):
            raise TypeError(f"'{token}' is not a valid Telegram Bot API Token!")
        
        self.token = token
        """
        Your Bot API token. 
        """

        self.user_id = int(self.token.split(":", 1)[0])
        """
        The user ID of the bot.
        """
        
        if event_manager and not isinstance(event_manager, EventManager):
            raise TypeError("`event_manager` has to be an instance of `EventManager`")
        
        self.event = event_manager or EventManager()
        """
        The event manager of the bot.

        See [Events](https://github.com/SwissCore92/swisscore-tba-lite?tab=readme-ov-file#events) 
        and [Temporary Events](https://github.com/SwissCore92/swisscore-tba-lite?tab=readme-ov-file#temporary-events)
        for more info.
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
        
        self.client: httpx.AsyncClient | None = None
        """
        The async client is initialized when the bot is started.  
        
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
        
        self.default_timeout: int = 30
        """
        Default timeout to use for requests (if not provided in __call__).
        """
        
        self.max_timeout: int = 60
        """
        Limits the max timeout for retrying timed out requests.
        """
        
        self._tasks: list[asyncio.Task] = []
        """
        Stores currently running tasks to protect them from beeing collected by the garbage collector.  
        
        **Is used internally to manage tasks**
        """

        self._is_ready: bool = False
        """
        Is True when polling (or listening in webhook mode) begins but after 'startup' event

        **Is used internally to check if the bot is fully started**
        """

        self.__rate_control = asyncio.Semaphore(max_concurrent_requests)

    #region tasks
    
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
    
    #endregion tasks
    
    #region core

    def download(self, file: objects.File) -> FileDownloader:
        if not isinstance(file, dict):
            raise TypeError(f"File obj expected (dict). Got {type(file)}.")
        
        if "file_path" not in file:
            raise KeyError(f"Invalid File object. Field `file_path` not found.")

        return FileDownloader(f"{self.file_url}/{file["file_path"]}", self.client)

    def __call__(
        self, 
        method_name: literals.MethodName, 
        params: JsonDict | None = None,
        *, 
        check_input_files: list[str] | None = None, 
        check_input_media: dict[str, list[str]] | None = None,
        convert_func: t.Callable[[t.Any], T] | None = None,
        **kwargs
    ) -> asyncio.Task[T]:
        """
        Use this method to make [API](https://core.telegram.org/bots/api) requests.
        
        Returns a asyncio.Task which can be awaited to get actual result.  
        """

        if self.client is None:
            # TODO: Maybe use custom exception for uninitialized client  
            raise RuntimeError("Async client is not initialized.")
        
        timeout: int | None = kwargs.get("timeout", None)
        auto_prepare: bool = kwargs.get("auto_prepare", True)
        catch_errors: bool = kwargs.get("catch_errors", True)

        @request_task_wrapper(catch_errors=catch_errors, rate_control=self.__rate_control)
        async def request():
            nonlocal params
            nonlocal timeout

            files: dict[str, tuple[str, bytes, str]] | None = None
            if params and (check_input_files or check_input_media):
                # may raise a FileProcessingError
                params, files = await prepare_files(params, check_input_files, check_input_media)
                    
            if auto_prepare and params:
                # may raise an InvalidParamsError
                params = serialize_params(params)

            if not params:
                # ensure params is not an empty dict
                params = None

            if method_name.lower() in USE_CLOUD_URL:
                url = f"{CLOUD_BOT_API_URL}/bot{self.token}/{method_name}"
            else:
                url = f"{self.api_url}/{method_name}"
            
            retries = 0

            while retries < self.max_retries:
                
                if timeout is not None:
                    timeout = min(timeout, self.max_timeout)
            
                try:
                    r = await self.client.post(url, data=params, files=files, timeout=timeout or httpx.USE_CLIENT_DEFAULT)

                    exceptions.raise_for_telegram_error(method_name, r)
                    
                    response: JsonDict = r.json()

                    if self.log_successful_requests:
                        logger.debug(f"'{method_name}' -> HTTP {r.status_code}: OK")
                    
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
                        logger.warning(f"{e} - Retrying after {e.retry_after} seconds... "
                            f"({self.max_retries - retries} / {self.max_retries} retries left.)"
                        )
                        await asyncio.sleep(e.retry_after)
                        retries += 1
                        continue
                    
                    raise
                
                except (asyncio.TimeoutError, httpx.TimeoutException) as e:
                    wait_time = 2**retries
                    logger.warning(f"'{method_name}' timed out. - Retrying after {wait_time} seconds... "
                        f"({self.max_retries - retries} / {self.max_retries} retries left.)"
                    )
                    await asyncio.sleep(wait_time)
                    timeout += 10
                    retries += 1
                    continue
                
                except (httpx.ConnectError, httpx.RemoteProtocolError) as e:
                    wait_time = 2**retries
                    logger.warning(f"'{method_name}' Network issue detected. Check your internet connection. Retrying in {wait_time} seconds... "
                        f"({self.max_retries - retries} / {self.max_retries} retries left.)"
                    )
                    await asyncio.sleep(wait_time)
                    timeout += 10
                    retries += 1
                    continue
                
                except Exception as e:
                    # Unexpected Error. raise.  
                    raise
            
            raise exceptions.MaxRetriesExeededError(f"'{method_name}' Max retries exceeded. Request failed.")
        
        return self._create_task(request(), name=method_name)

    async def process_update(self, update: JsonDict) -> None:
        """
        Process an Update by triggering the corresponding event handler. 
        """
        try:
            update_id = update["update_id"]
            update_type = utils.get_update_type(update)
            update_object = update[update_type]
            
            await self.event._trigger_event(update_type, update_object, update_id)
        
        except exceptions.RestartBotException as e:
            logger.debug(f"{repr(e)} raised. Preparing Shutdown.")
            setattr(self, "restart_flag", True)


    #endregion core

    #region polling
    
    def start_polling(
        self, 
        drop_pending_updates: bool = False
    ) -> None:
        """
        Start the bot in [long polling](https://en.wikipedia.org/wiki/Push_technology#Long_polling) mode.  
        
        Uses the [`getUpdates`](https://core.telegram.org/bots/api#getupdates) API method to get [Updates](https://core.telegram.org/bots/api#update).  
        
        **Note:**
        * *`offset`* is calculated automatically
        * *`limit`* can be set using `bot.update_limit = <limit>` (defaults to `None` which is 100)
        * *`timeout`* can be set using `bot.polling_timeout = <timeout>` (defaults to 20)
        * *`allowed_updates`* are automatically set, based on your event handlers

        Shorthand for:
        ```python
        asyncio.run(bot._polling_loop(...))
        ```
        
        """
        logger.debug("Start async event loop")

        asyncio.run(self._polling_loop(drop_pending_updates))

        logger.debug("Closed async event loop")

    async def _polling_loop(self, drop_pending_updates: bool = False) -> None:
        """
        Wait for incoming updates and trigger the matching event handlers.  
        
        To start polling use 
        ```python
        bot.start_polling(...)
        ```
        > *or*
        ```python
        asyncio.run(bot._polling_loop(...))
        ```
        """
        exit_code: int = 0

        self.event._lock()
        
        logger.debug("Start async client")

        offset = 0

        async with httpx.AsyncClient(timeout=self.default_timeout) as client:
            self.client = client
            if drop_pending_updates:
                if updates := await self.__call__("getUpdates", params={"offset": -1}, auto_prepare=False):
                    logger.debug("Dropped pending updates.")
                    offset = updates[-1]["update_id"] + 1
            
            await run_builtin_event(self, "startup")
            
            logger.info(f"Start Bot in long polling mode. Press {utils.kb_interrupt()} to quit.")
            # logger.debug(f"Allowed updates: {params["allowed_updates"]}")

            self._is_ready = True

            while True:
                try: 
                    if getattr(self.event, "restart_flag", False) is True:
                        exit_code = exit_codes.RESTART
                        logger.info(f"RestartBotException raised. Shutting down with {exit_code=}.")
                        break

                    params = {
                        "offset": offset, 
                        "allowed_updates": self.event._get_handled_event_types(), 
                        "timeout": self.polling_timeout,
                        "limit": self.update_limit
                    }
                    if updates := await self.__call__("getUpdates", params=params, catch_errors=False):
                        logger.debug(f"Received {len(updates)} new update(s).")

                        for update in updates:
                            await self.process_update(update)
                            offset = update["update_id"] + 1

                except exceptions.MaxRetriesExeededError as e:
                    logger.error(f"Failed to get updates. Check your Internet Connection. Retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                
                except asyncio.CancelledError:
                    exit_code = exit_codes.TERMITATED_BY_USER
                    logger.info(f"Shutting down with {exit_code=}.")
                    break
                
                except exceptions.TelegramAPIError as e:
                    if e.critical:
                        # Only happens when '409: Conflict' or '403: Forbidden' is raised
                        exit_code = exit_codes.CRITICAL_TELEGRAM_ERROR
                        logger.critical(f"Shutting down with {exit_code=}.")
                            
                    else:
                        # Should not happen in theory. (The getUpdate request was invalid, logging with exc_info)
                        logger.critical(f"Failed to get updates due an unexpected Telegram API Error. {repr(e)}", exc_info=True)
                        exit_code = exit_codes.UNEXPECTED_TELEGRAM_ERROR
                        
                    break
                
                except Exception as e:
                    exit_code = exit_codes.UNEXPECTED_ERROR
                    logger.critical(f"A critical, unexpected error occured. Shutting down with {exit_code=}.", exc_info=True)
                    break
            
            await run_builtin_event(self, "shutdown", exit_code)

        self.client = None
        logger.debug("Closed async client")
        if getattr(self, "restart_flag", False):
            subprocess.run([sys.executable, *sys.argv])
            exit()

    #endregion polling
    
    #region idle

    def start_idle(self) -> None:
        """
        Start the bot in idle mode (for webhooks). 
        
        The bot will do nothing but waiting for updates commited to it using `bot.process_update(update)`.    

        Shorthand for:
        ```python
        asyncio.run(bot._idle_loop())
        """
        logger.debug("Start async event loop")

        asyncio.run(self._idle_loop())

        logger.debug("Closed async event loop")
    
    async def _idle_loop(self) -> None:
        """
        Wait for updates being commited by using `bot.process_update(update)`.  
        
        To start idle use 
        ```python
        bot.start_idle()
        ```
        > *or*
        ```python
        asyncio.run(bot._idle_loop())
        ```
        """

        

        exit_code: int = 0
        
        logger.debug("Start async client")

        async with httpx.AsyncClient(timeout=self.default_timeout) as client:
            self.client = client

            await run_builtin_event(self, "startup")
            
            logger.info(f"Start Bot in idle mode. Press {utils.kb_interrupt()} to quit.")

            self._is_ready = True
            
            while True:
                try: 
                    # sleep at an inteval of 3600 seconds (1 hour)
                    await asyncio.sleep(3600)
                
                except asyncio.CancelledError:
                    exit_code = exit_codes.TERMITATED_BY_USER
                    logger.info(f"Shutting down with {exit_code=}.")
                    break
                
                except Exception as e:
                    exit_code = exit_codes.UNEXPECTED_ERROR
                    logger.critical(f"A critical, unexpected error occured. Shutting down with {exit_code=}.", exc_info=True)
                    break
            
            await run_builtin_event(self, "shutdown", exit_code)

        self.client = None
        logger.debug("Closed async client")
        if getattr(self, "restart_flag", False):
            subprocess.run([sys.executable, *sys.argv])
            exit()

    #endregion idle
