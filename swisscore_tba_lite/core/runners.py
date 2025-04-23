
import typing as t
import atexit
import asyncio
import threading
import time
from abc import ABC, abstractmethod

from .base_bot import BaseBot
from .logger import logger

class AbstractRunner(ABC):
    def __init__(self, bot) -> None:
        if not isinstance(bot, BaseBot):
            raise TypeError("bot has to be an instance of BaseBot")
        self.bot: BaseBot = bot
        self._started = False
        self._stopped = False

        atexit.register(self._check_proper_shutdown)

    @abstractmethod
    def start_polling(self) -> None: ...

    @abstractmethod
    def start_idle(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    def _check_proper_shutdown(self):
        if self._started and not self._stopped:
            logger.warning(
                f"{self.__class__.__name__} was not properly stopped or used as a context manager."
            )

class ThreadedRunner(AbstractRunner):
    """
    A bot runner to run the bot in a background thread in blocking applications (like a flask app).

    Example Usage:
    ```python
    
    from flask import Flask
    from swisscore_tba_lite import BaseBot as Bot, ThreadedRunner

    bot = Bot("your_token")

    app = Flask(__name__)
    
    @app.route("/")
    def home():
        ...

    @bot.event("message")
    async def on_message(msg):
        ...

    def main():
        with ThreadedRunner(bot) as runner:
            runner.start_polling()
            app.run(...) # <- never use `debug=True` using this setup. The restarts will confuse the runner

    if __name__ == "__main__":
        main()
    ```

    """
    def __init__(self, bot: BaseBot):
        super().__init__(bot)
        self._thread: threading.Thread | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._main_task: asyncio.Task[None] | None = None
    
    def __enter__(self) -> "ThreadedRunner":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_val:
            logger.error(f"Error in main thread: {repr(exc_val)}")
        if self._started and not self._stopped:
            self.stop()
        elif not self._started                                                :
            logger.warning(
                f"{self.__class__.__name__} context exited, but runner was never started."
            )

    def __start(self, coro, *args) -> None:
        if self._started:
            raise RuntimeError("the runner can only be started once.")

        self._started = True

        def thread_target() -> None:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._main_task = self._loop.create_task(
                coro(*args)
            )
            try:
                self._loop.run_until_complete(self._main_task)
            except asyncio.CancelledError:
                pass
            finally:
                self._loop.run_until_complete(self._loop.shutdown_asyncgens())
                self._loop.close()

        self._thread = threading.Thread(target=thread_target, daemon=True)
        
        logger.debug(f"{self.__class__.__name__} starting...")

        self._thread.start()

        # Waiting until the bot has finished startup
        while not self.bot._is_ready:
            time.sleep(0.1)

    def start_polling(self, drop_pending_updates: bool = False) -> None:
        self.__start(self.bot._polling_loop, drop_pending_updates)
    
    def start_idle(self) -> None:
        self.__start(self.bot._idle_loop)

    def stop(self) -> None:
        if self._loop and self._loop.is_running():
            logger.debug(f"{self.__class__.__name__} stopping...")
            def cancel() -> None:
                if self._main_task:
                    self._main_task.cancel()
            self._loop.call_soon_threadsafe(cancel)
            self._thread.join()
            self._stopped = True

# class AsyncRunner(AbstractRunner):
#     """
#     A bot runner to run the bot in a background task in async applications (like an aiohttp web app).

#     Example Usage:
#     ```python
#     from aiohttp import web

#     from swisscore_tba_lite import BaseBot as Bot, AsyncRunner

#     bot = Bot("your_token")

#     webhook = web.Application()
#     routes = web.RouteTableDef()

#     @routes.get("/")
#     async def home(request):
#         ...
    
#     @bot.event("message")
#     async def on_message(msg):
#         ...

#     async def main():
#         with AsyncRunner(bot) as runner:
#             runner.start_polling()
#             web.run_app(app)

#     if __name__ == "__main__":
#         asyncio.run(main())
#     """
#     def __init__(self, bot: BaseBot):
#         super().__init__(bot)
#         self._main_task: asyncio.Task[None] | None = None
    
#     async def __aenter__(self) -> "AsyncRunner":
#         return self

#     async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
#         if exc_val:
#             logger.error(f"Error in main thread ({repr(exc_val)}). Shutting down.")
#         if self._started and not self._stopped:
#             await self.stop()
#         elif not self._started:
#             logger.warning(
#                 f"{self.__class__.__name__} context exited, but runner was never started."
#             )
    
#     async def __start(self, coro, *args) -> None:
#         if self._started:
#             raise RuntimeError("polling can only be started once.")
#         self._started = True
#         logger.debug(f"{self.__class__.__name__} starting...")
#         self._main_task = asyncio.create_task(
#             coro(*args)
#         )

#         # Waiting until the bot has finished startup
#         while not self.bot._is_ready:
#             await asyncio.sleep(0.1)

#     async def start_polling(self, drop_pending_updates: bool = False) -> None:
#         await self.__start(self.bot._polling_loop, drop_pending_updates)
    
#     async def start_idle(self):
#         await self.__start(self.bot._idle_loop)

#     async def stop(self) -> None:
#         if self._main_task:
#             logger.debug(f"{self.__class__.__name__} stopping...")
#             self._main_task.cancel()
#             try:
#                 await self._main_task
#             except asyncio.CancelledError:
#                 pass
#             self._stopped = True
        
        
