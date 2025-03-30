import asyncio
import typing as t
from json import JSONDecodeError
 
import aiohttp

from .. import utils
from .logger import logger
from .event import EventManager, EventHandlerError, FilterEvaluationError

class FailedRequestError(Exception): ...
class MaxRetriesExeededError(Exception): ...

def api_method(
    name: str | None = None,
    *,
    check_input_files: list[str] | None = None,
    check_input_media: list[str] | None = None,
    convert_func: t.Callable[[t.Any], t.Any] | None = None,
):
    """
    decorator for api methods
    
    **❌ CAN ONLY BE APPLIED TO METHODS OF `BotAPI` OR IT'S SUBCLASSES**
    
    It's purpose is to make it very easy to extend the `BotAPI` class.
    
    **Ussage:**
    ```python
    
    class Bot(BotAPI):
        @api_method()
        def send_message(self, chat_id, text, ...):
            \"""No Code needed, the decorator handles the request\"""
        
        @api_method(check_input_files=["photo"])
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
            
            bot: BotAPI = params.pop("self")
            
            if not isinstance(bot, BotAPI):
                raise TypeError(f"This decorator can only be applied to instances of BotAPI.")
            
            return bot(
                method_name, 
                params=params,
                check_input_files=check_input_files,
                check_input_media=check_input_media,
                convert_func=convert_func,
            )
            
        return inner
    
    return wrapper


async def prepare_files(
    params: dict[str, t.Any], 
    check_input_files: list[str] | None = None, 
    check_input_media: list[str] | None = None,
) -> tuple[dict[str, t.Any] | None, aiohttp.FormData | None]:
    form_data: aiohttp.FormData | None = None
    
    check_input_files = check_input_files or []
    check_input_media = check_input_media or []
    
    if check_input_files or check_input_media:
    
        input_files = await utils.process_input_files(params, check_input_files)
        media_files, input_media = await utils.process_input_media(params, check_input_media)
        input_files.update(media_files) 

        if input_files:
            form_data = await utils.create_form_data(params, input_files)

    if form_data is not None:
        return None, form_data
    
    return params, None


class BotAPI:
    def __init__(
        self, 
        token: str, 
        *, 
        base_api_url: str = "https://api.telegram.org",
        base_file_url: str = "https://api.telegram.org/file",
        event_manager: EventManager | None = None
    ) -> None:
        
        self.event = event_manager or EventManager()
        """
        The event manager.
        
        Use this decorator to register events:
        
        **Ussage**
        ```python
        
        ```
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
        Max retries for transient request errors (`TooManyRequests`, `TimeoutError`).
        """
        
        self.max_connection_retries: int = 20
        """
        Max retries for connection errors.
        
        *currently not used*
        """
        
        self._tasks: list[asyncio.Task] = []
        """
        Stores currently running tasks to protect them from the garbage collector.  
        
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
        logger.debug("Start asycnc event loop")
        
        asyncio.run(self._polling_main_loop())
        
        logger.debug("Closed asycnc event loop")
    
    
    async def _polling_main_loop(self) -> None:
        """
        Iterates over incoming updates and triggers event handlers.  
        
        To start polling use 
        ```python
        bot.start_polling()
        ```
        > *or*
        ```python
        asyncio.run(bot._polling_main_loop())
        ```
        """
        async for update_type, obj in self._get_future_updates():
            try:
                await self.event._trigger_event(update_type, obj)
            
            except (FilterEvaluationError, EventHandlerError) as e:
                logger.error(f"Failed to process update of type '{update_type}'. Update was dropped. ({e})", exc_info=True)
    
    async def _get_future_updates(
        self,
        drop_pending_updates: bool = False
    ) -> t.AsyncGenerator[tuple[str, dict[str, t.Any]], None]:
        """
        Generator that asks repeatedly (in an interval of `bot.polling_timeout`) for new updates and yields them.  
        
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
            
            await self.event._trigger_event("startup")
            await self._gather_pending_tasks()
            
            logger.info(f"Start Bot in long polling mode. Press {utils.kb_interrupt()} to quit.")
            
            while True:
                try: 
                    if updates := await self.__call__("getUpdates", params=params, auto_prepare=False):
                        for update in updates:
                            update_type = utils.get_update_type(update)
                            yield update_type, update[update_type]
                    
                        params["offset"] = updates[-1]["update_id"] + 1

                except MaxRetriesExeededError as e:
                    logger.error(f"Failed to get updates. Check your Internet Connection. Retrying in 60 seconds...")
                    await asyncio.sleep(60)
                    continue
                
                except asyncio.exceptions.CancelledError:
                    exit_code = 0
                    logger.info(f"{utils.kb_interrupt()} pressed. Shutting down.")
                    break
                
                except FailedRequestError as e:
                    # Should not happen. (The getUpdate request was invalid)
                    logger.critical(f"Failed to get updates. {repr(e)}", exc_info=True)
                    exit_code = 4
                
                except Exception as e:
                    exit_code = 1
                    logger.critical("A critical, unexpected error occured. Shutting down.", exc_info=True)
                    break

            await self.event._trigger_event("shutdown", exit_code)
            await self._gather_pending_tasks()

        self.session = None
        logger.debug("Closed client session")


    def __call__(
        self, 
        method_name: str, 
        params: dict[str] | None = None,
        *,
        auto_prepare: bool = True,
        check_input_files: list[str] | None = None, 
        check_input_media: list[str] |None = None,
        timeout: int = 30,
        convert_func: t.Callable[[t.Any], t.Any] | None = None,
    ) -> asyncio.Task[dict[str] | t.Any]:
        """
        Use this method to make [API](https://core.telegram.org/bots/api) requests.

        **Ussage:**
        ```python
        bot("sendMessage", {"chat_id": chat_id, "text": "Hello world!"})
        me = await bot("getMe") 
        ```
        
        Returns a asyncio.Task which can be awaited to get the result.
        
        """
        
        if self.session is None:
            raise RuntimeError("Client session is not initialized.")

        async def request():
            nonlocal params

            data: aiohttp.FormData | None = None
            if params and (check_input_files or check_input_media):
                try:
                    params, data = await prepare_files(params, check_input_files, check_input_media)

                except FileNotFoundError:
                    logger.error(f"Provided file in was not found. - {method_name}({params=}", exc_info=True)
                    raise
                
                except IOError:
                    logger.error(f"Error occured while reading file. - {method_name}({params=}", exc_info=True)
                    raise
                
                except Exception as e:
                    logger.critical(f"A unexcepted error occured while preparing files. - {method_name}({params=}", exc_info=True)
                    raise
                    
            if auto_prepare and params:
                params = {
                    k: utils.dumps(v) if isinstance(v, (dict, list, tuple)) else v
                    for k, v in params.items() 
                    if v is not None
                }
            
            url = f"{self.api_url}/{method_name}"
            
            request_info = f"{method_name}({params=}, {data=})"
            
            retries = 0

            while retries < self.max_retries:
            
                try:
                    async with self.session.post(
                        url, 
                        params=params, 
                        data=data, 
                        timeout=timeout,
                    ) as r:
                        response: dict[str] = await r.json()
                        
                        if response["ok"]:
                            result = response["result"]
                            
                            if self.log_successful_requests:
                                logger.debug(f"Succeeded Request: {request_info} -> {result}")
                                
                            if callable(convert_func):
                                try:
                                    result = convert_func(result)
                                except Exception as e:
                                    logger.error(f"Conversion of result failed! ", exc_info=True)
                                    raise 
                            else:
                                return result 
                        
                        else:
                            if parameters := response.get("parameters"):
                                if wait_time := parameters.get("retry_after"):
                                    if retries < self.max_retries:
                                        logger.warning(f"Rate-limited! Retrying after {wait_time} seconds...")
                                        await asyncio.sleep(wait_time)
                                        retries += 1
                                        continue
                            
                                elif migrate_to_chat_id := parameters.get("migrate_to_chat_id"):
                                    # TODO: try handle migrate_to_chat_id instead of raising failed request error
                                    raise FailedRequestError(f"Failed Request: {request_info} -> {migrate_to_chat_id=}")
                            
                            elif description := response.get("description"):
                                raise FailedRequestError(f"Failed Request: {request_info} -> {description=}")
                            
                            else:
                                # Should never happen. But to be save we raise failed request error here, to avoid infinite loop.
                                raise FailedRequestError(f"Failed Request: {request_info} -> {response}")
                
                except JSONDecodeError as e:
                    logger.error(f"{request_info} - Error while decoding response json. {repr(e)}")
                    raise FailedRequestError(f"{request_info} - Error while decoding response json. {repr(e)}") from e
                
                except FailedRequestError as e:
                    logger.error(repr(e), exc_info=True)
                    raise
                
                except TimeoutError as e:
                    wait_time = 2**retries
                    logger.warning(f"{request_info} timed out. Retrying after {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    retries += 1
                    continue
                
                except (
                    aiohttp.ClientConnectionError, 
                    aiohttp.ServerConnectionError, 
                    aiohttp.ClientOSError
                ) as e:
                    wait_time = 2**retries
                    logger.warning(f"{request_info} network error. Retrying after {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    retries += 1
                    continue
                
                except Exception as e:
                    logger.critical(f"{request_info} - An unecpected error ocured: ", exc_info=True)
                    raise
            
            logger.error(f"Max retries reached for {request_info}. Request failed.")
            raise MaxRetriesExeededError(f"Max retries reached for {request_info}. Request failed.")
        
        return self._create_task(request(), name=method_name)
    
