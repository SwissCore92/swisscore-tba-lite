"""
## **SwissCore TBA Lite**
A minimal, async-native **Telegram Bot API** library — built for developers who want power without the clutter.

*See [docs](https://github.com/SwissCore92/swisscore-tba-lite) on GitHub for more info.*
"""

from .core.base_bot import BaseBot
from .core.logger import logger
from .core.exceptions import RestartBotException
from .core.runners import ThreadedRunner

from .bot_api import objects
from .bot_api import Bot
