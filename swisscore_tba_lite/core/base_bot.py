import asyncio
import typing as t
import subprocess
import sys
import os
from functools import wraps
from pathlib import Path

import aiohttp
import aiofiles

from .. import utils
from .logger import logger
from .event import EventManager
from . import exit_codes
from . import exceptions

T = t.TypeVar("T")
JsonDict = dict[str, t.Any]

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
async def prepare_files(
    params: JsonDict, 
    check_input_files: list[str] | None = None, 
    check_input_media: list[str] | None = None,
) -> tuple[JsonDict | None, aiohttp.FormData | None]:
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
        base_api_url: str = "https://api.telegram.org",
        base_file_url: str = "https://api.telegram.org/file",
        event_manager: EventManager | None = None
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
        
        if event_manager and not isinstance(event_manager, EventManager):
            raise TypeError("`event_manager` has to be an instance of `EventManager`")
        
        self.event = event_manager or EventManager()
        """
        The event manager of the bot.
        
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
        
        self.default_timeout: int = 30
        """
        Default timeout to use for requests (if not provided in __call__).
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

        self._is_ready: bool = False
        """
        Is True when polling (or listening in webhook mode) begins but after 'startup' event

        **Is used internally to check if the bot is fully started**
        """

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
    
    def download(
        self, 
        file_obj: JsonDict, 
        dest_dir: str | Path | None = None, 
        file_name: str | None = None,
        *,
        overwrite_existing: bool = False, 
        bs: int | None = None,
    ) -> asyncio.Task[Path]:
        """Download a file from telegram server.
        
        **Note: The file must be fetched from telegram first using the `getFile` method**
        
        Example Usage:
        ```python
        # filtering messages with document 
        @bot.event("message", filters=[is_document, lambda m: m["document"].get("file_name")])
        async def on_document_message(msg: dict[str]):
            doc = msg["document"]
            file_obj = await bot("getFile", {"file_id": doc["file_id"]})
            file_path = await bot.download(file_obj, Path.cwd() / ".tmp", doc["file_name"], overwrite_existing=True)
        ```

        Args:
            file_obj (JsonDict): The file object received by using `getFile` api method.
            dest_dir (str | Path | None, optional): The destination directory. Defaults to Current working directory `Path.cwd()` (Usually the location of your script).
            file_name (str | None, optional): The destination file name (**with suffix** eg. *'document.txt' **not** 'document'*). Defaults to `file_obj['file_name'] if present else the name in file_obj['file_path']`.
            overwrite_existing (bool, optional): If set to `True` and the file already exists, the file is overwritten. Else a `FileExistsError` is raised. Defaults to `False`.
            bs (int, optional): The chunk size for the download in bytes. If `bs <= 0`, the file is downloaded as a whole. Defaults to 16KiB (16384)
        Raises:
            KeyError: if `file_path` not found in `file_obj`
            NotADirectoryError: if dest_dir is not a directory
            FileNotFoundError: if dest_dir is not found
            FileExistsError: if destination file already exists and `overwrite_existing` is `False`
            TelegramError: if the download fails for some reason

        Returns:
            Task[Path]: A scheduled task that downloads the file.
        """
        if not "file_path" in file_obj:
            raise KeyError("'file_path' is not present in file_obj. Did you get the file correctly using 'getFile'?")
        
        if dest_dir is None:
            dest_dir = Path.cwd()
        elif isinstance(dest_dir, str):
            dest_dir = Path(dest_dir)
        
        if not dest_dir.exists():
            raise FileNotFoundError(f"{dest_dir=} was not found.")
        if not dest_dir.is_dir():
            raise NotADirectoryError(f"{dest_dir=} is not a directory.")
        
        tg_file_path: str = file_obj["file_path"]
        
        if file_name is None:
            file_name: str = file_obj.get("file_name", tg_file_path.rsplit("/", 1)[-1])
            
        dest_file = dest_dir / file_name
        
        if dest_file.exists():
            if not overwrite_existing:
                raise FileExistsError(f"{dest_file=} already exists and overwriting is not allowed.")
            # No warning needed. the user decided to overwrite
            # logger.warning(f"'<dest_dir>/{file_name}' will be overwritten!")
        
        bs = bs or 16*utils.KiB
        
        file_size = file_obj.get("file_size", 0)

        async def _download_file():
            async with aiofiles.open(dest_file, "wb") as f:
                
                async with self.session.get(f"{self.file_url}/{tg_file_path}") as r:
                    
                    logger.debug(f"Start downloading '<dest_dir>/{file_name}' "
                        f"(Predicted Size: {utils.readable_file_size(file_size)})"
                    )
                    
                    await exceptions.raise_for_telegram_error("DownloadFile", r)
                    
                    if bs <= 0:
                        await f.write(await r.content.read())
                    
                    else:
                        async for chunk in r.content.iter_chunked(bs):
                            await f.write(chunk)
                
                logger.debug(f"Successfully downloaded '<dest_dir>/{file_name}' "
                    f"(Size: {utils.readable_file_size(os.stat(dest_file).st_size)})"
                )
        
            return dest_file

        return self._create_task(_download_file())

    def __call__(
        self, 
        method_name: str, 
        params: JsonDict | None = None,
        *, 
        check_input_files: list[str] | None = None, 
        check_input_media: list[str] | None = None,
        convert_func: t.Callable[[t.Any], T] | None = None,
        timeout: int | None = None,
        **kwargs
    ) -> asyncio.Task[T]:
        """
        Use this method to make [API](https://core.telegram.org/bots/api) requests.
        
        Returns a asyncio.Task which can be awaited to get actual result.  

        **Ussage:**
        ```python
        bot("sendMessage", {"chat_id": chat_id, "text": "Hello world!"})
        me = await bot("getMe") 
        ```
        
        Note: `JsonDict` is just a shorthand for `dict[str, Any]`

        > ⚠️ ***Warning:***  
        > * *Using this method when the bot isn't yet started will raise a `RuntimeError`! Use the 'startup' event if you need to make requests on startup!*  
        
        """

        if self.session is None:
            # TODO: Maybe use custom exception for uninitialized session  
            raise RuntimeError("Client session is not initialized.")
        
        timeout = timeout or self.default_timeout
        auto_prepare: bool = kwargs.get("auto_prepare", True)
        catch_errors: bool = kwargs.get("catch_errors", True)

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
                params = serialize_params(params)

            url = f"{self.api_url}/{method_name}"
            
            retries = 0

            while retries < self.max_retries:
                
                timeout = min(timeout, self.max_timeout)
            
                try:
                    async with self.session.post(
                        url, 
                        json=params, 
                        data=data, 
                        timeout=timeout,
                    ) as r:
                        
                        await exceptions.raise_for_telegram_error(method_name, r)
                        
                        response: JsonDict = await r.json()

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
                
                except (asyncio.TimeoutError, aiohttp.ServerConnectionError) as e:
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

    async def process_update(self, update: JsonDict) -> None:
        """
        Process an Update by triggering the corresponding event handler. 
        """
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
        
        except exceptions.RestartBotException as e:
            logger.debug(f"{repr(e)} raised. Preparing Shutdown.")
            setattr(self, "restart_flag", True)
        
        except exceptions.FilterEvaluationError as e:
            logger.error(f"Failed to process update of type '{update_type}'. Update was dropped. ({e})", exc_info=True)
        
        except exceptions.EventHandlerError as e:
            logger.error(f"A event handler processing an update of type '{update_type}' crashed. ({e})", exc_info=True)
    
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
        
        params = {
            "offset": 0, 
            "limit": self.update_limit, 
            "timeout": self.polling_timeout,
            "allowed_updates": utils.dumps(self.event._get_handled_event_types())
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        logger.debug("Start client session")

        async with aiohttp.ClientSession() as session:
            self.session = session
            if drop_pending_updates:
                if updates := await self.__call__("getUpdates", params={"offset": -1}, auto_prepare=False):
                    logger.debug("Dropped pending updates.")
                    params["offset"] = updates[-1]["update_id"] + 1
            
            await run_builtin_event(self, "startup")
            
            logger.info(f"Start Bot in long polling mode. Press {utils.kb_interrupt()} to quit.")
            logger.debug(f"Allowed updates: {params["allowed_updates"]}")

            self._is_ready = True
            
            while True:
                try: 
                    if updates := await self.__call__("getUpdates", params=params, auto_prepare=False, catch_errors=False):
                        logger.debug(f"Received {len(updates)} new update(s).")

                        for update in updates:
                            await self.process_update(update)
                            params["offset"] = update["update_id"] + 1
                        
                        if getattr(self, "restart_flag", False):
                            await self.__call__("getUpdates", {"offset": params["offset"], "timeout": 0})
                            exit_code = exit_codes.RESTART
                            logger.info(f"RestartBotException raised. Shutting down with {exit_code=}.")
                            break
                        
                        elif getattr(self, "shutdown_flag", False):
                            logger.info(f"Shutdown raised. Shutting down with {exit_code=}.")

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

        self.session = None
        logger.debug("Closed client session")
        if getattr(self, "restart_flag", False):
            python = sys.executable
            subprocess.run([python] + sys.argv)
            exit()

    #endregion polling
    
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
        
        logger.debug("Start client session")

        async with aiohttp.ClientSession() as session:
            self.session = session

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

        self.session = None
        logger.debug("Closed client session")
        if getattr(self, "restart_flag", False):
            python = sys.executable
            subprocess.run([python] + sys.argv)
            exit()
