"""
# **SwissCore TBA Lite**
![Python](https://img.shields.io/badge/python-3.11%2B-blue)  

A very basic and lightweight asynchronous [Telegram Bot API](https://core.telegram.org/bots/api) wrapper for **python 3.11+**.  
Main focus on core functionality without all the bloat. Just *dictionaries*.  

*Read full [docs on GitHub](https://github.com/SwissCore92/swisscore-tba-lite)*
"""

from .core.base_bot import BaseBot as Bot
from .core.logger import logger
from .core.exceptions import RestartBotException