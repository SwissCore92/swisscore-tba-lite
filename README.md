# **SwissCore TBA Lite**
![Python](https://img.shields.io/badge/python-3.11%2B-blue)  

A very basic and lightweight asynchronous [Telegram Bot API](https://core.telegram.org/bots/api) wrapper for **python 3.11+**.  
Focuses on core functionality and easy expandability.  

> ⚠️ **Note:** *This project is work in progress!*  

Handles just in *dictionaries*. 

* [Features](#features)
    * [Automatc file processing](#automatc-file-processing)
    * [Expandability](#expandability)
* [Installation](#installation)
* [Quick Start](#quick-start)

## Features

The purpose of this Repository is to build a stable and powerful base for Telegram Bots. But it can also be used directly by advanced users, well knowing the Telegram Bot API. It is completely written in python 3.13, using modern python techniques.

### Automatc file processing

Simple things like file processing are done automatically by the bot. Eg. `InputFile` and the `media` field of `InputMedia` can just be a `str` representing a Path, a `pathlib.Path` or just `bytes`. The bot will process this automatically if the `check_input_files` or `check_input_media` are set properly.

Eg.
```python
from pathlib import Path

m = await bot("sendPhoto", {
    "chat_id": chat_id,
    "photo": "path/to/photo.png",
    "caption": "My beautiful picture"
}, check_input_files=["photo"])

bot("editMessageMedia", {
    "chat_id": chat_id,
    "message_id": m["message_id"],
    "media": {
        "type": "photo", 
        "media": "path/to/another_photo.png"
    }
}, check_input_media=["media"])

bot("sendMediaGroup", {
    "chat_id" chat_id,
    "media": [
        {"type": "photo", "media": "path/to/photo1.png"},
        {"type": "photo", "media": photo2_bytes},
        {"type": "photo", "media": Path("path/to/photo3.png")},
        {"type": "photo", "media": "path/to/photo4.png"},
    ]
}, check_input_media=["media"])
```

### Expandability

It's very easy to make a user friendlier bot, using this Bot as base.

Eg.
```python
from swisscore_tba_lite.core.base_bot import BaseBot, api_method

# Make a class representing a Message
class Message:
    def __init__(self, message_id: int, ...):
        ...

# Make a class inheriting from `BaseBot` to add user frendlier methods
class Bot(BaseBot):
    @api_method(
        check_input_files=["photo"], 
        convert_func=lambda m: m if m is True else Message(**m)
    )
    def send_photo(chat_id: int, photo: str | Path | bytes, ...) -> Message | Literal[True]:
        """
        No code required. the decorator handles the request.
        The method name is automatically converted to camel case.
        Due to `check_input_files=["photo"]`, 
          the photo is automatically processed.
        If it is a valid strPath, Path or bytes. 
        A str representing a Telegram file_id 
          or an url can still be passed. 
        convert_func converts the api call result
          to a Message instance. 
        You can pass any convertion function you like.
        """

bot = Bot(<TOKEN>)

@bot.event("startup")
async def startup()
    msg = await bot.send_photo(...)

bot.start_polling()
```

## Installation

*Requires Python 3.11+*

### Installation on Windows  
```sh
python -m pip install git+https://github.com/SwissCore92/swisscore-tba-lite.git
```

### Installation on Linux / MacOS   
```sh
python3 -m pip install git+https://github.com/SwissCore92/swisscore-tba-lite.git
```

## Quick Start

```python
import os 

from swisscore_tba_lite import Bot
from swisscore_tba_lite.filters import commands, chat_types

# Get your Telegram Bot API Token from @BotFather
# Set it in an environment variable (API_TOKEN) 
#   or manually replace <YOUR_API_TOKEN> below
TOKEN = os.environ.get("API_TOKEN", "<YOUR_API_TOKEN>")

# Get your Telegram user ID
# (if you don't know it,
#   you can use the `/myid` command below in private chat with your bot)
# Set it in an environment variable (ADMIN_ID) 
#   or manually replace 1234 below
ADMIN_ID = int(os.environ.get("ADMIN_ID", 1234))

# Initialize the bot with your token
bot = Bot(TOKEN)

# Add a startup handler.
@bot.event("startup")
async def on_startup():
    """
    Runs on bot startup.  
    Sends a message to the admin indicating the bot has started.
    """
    bot("sendMessage", {
        "chat_id": ADMIN_ID, 
        "text": "Hi, I was just started!"
    })

# Add a message handler for private messages with the commamd /myid
@bot.event("message", filters=[chat_types("private"), commands("myid")])
async def on_cmd_myid(msg: dict[str]):
    """
    Runs when a user sends '/myid' in a private chat with the bot.  
    Sends the user's ID back to them.
    """
    user_id = msg["from"]["id"]
    bot("sendMessage", {
        "chat_id": user_id, 
        "text": f"Your user ID is `{user_id}`",
        "parse_mode": "MarkdownV2"
    })

# Add a shutdown handler.
@bot.event("shutdown")
async def on_shutdown(exit_code: int):
    """
    Runs when the bot shuts down.  
    Sends a message to the admin indicating the bot has stopped.
    """
    if exit_code == 0:
        bot("sendMessage", {
            "chat_id": ADMIN_ID, 
            "text": "Bye, I was just shut down!"
        })

# Start the bot in long polling mode
# This starts an async event loop and blocks the code.
bot.start_polling()
