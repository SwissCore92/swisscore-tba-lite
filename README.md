# **SwissCore TBA Lite**
![Python](https://img.shields.io/badge/python-3.11%2B-blue)  

A very lightweight *asynchronous* [Telegram Bot API](https://core.telegram.org/bots/api) wrapper for **python 3.11+**.  
Main focus on core functionality without all the bloat. Just *dictionaries*.  

✅ **Very flexible**  
✅ **Very fast**  
✅ **No bloat**  
✅ **Easy to extend**  
✅ **Builin colored Logger** *(requires colorama)*  
✅ **Written from scratch in modern Python using modern techniques**  

> ⚠️ **Note:** *This project and it's documentation are still work in progress!*  
> * *I don't recommed to use it until it is released on PyPI!*
> * *A production ready release will follow soon.*
> * *This documentation will be improved over time.*


* [Installation](#installation)
* [Quick Start](#quick-start)
* [Automatic file processing](#automatic-file-processing)
* [Expandability](#expandability)
* [Tasks](#tasks)
* [Events](#events)
* [Flexible Filter Composition System](#flexible-filter-composition-system)
* [Event Handler Chaining](#event-hanlder-chaining)


## Installation

*Requires Python 3.11+*

### Create and activate a virtual Environment
While this is optional, it's highly recommended to use a virtual environment to avoid conflicts with other Python projects.  
It's also a save place to store your Telegram Bot API token.

Open a Terminal in a work directory of your choice.

```sh
python -m venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate
```
> 💡 Remember to activate the virtual environment every time you work on your bot or on the project itself.

Set your Bot API token in an environment variable.
The token looks something like `123456:ABC-DEF1234ghIkl_zyx57W2v1u123ew11` but we use `token` in this example.

```sh
# Linux/macOS
export API_TOKEN=token

# Windows
set API_TOKEN=token        
```

### Installation

Since there is no PyPI release at the moment, you have to install it from source using `pip` & `git`.
```sh
pip install git+https://github.com/SwissCore92/swisscore-tba-lite.git
```
*Note: on Linux/MacOs you may have to use `pip3`*

### Editable Install (For Development)
```sh
git clone https://github.com/SwissCore92/swisscore-tba-lite.git
cd swisscore-tba-lite
pip install -e .
```
*Note: on Linux/MacOs you may have to use `pip3`*


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
```

## Automatic file processing

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

It also comes with a builtin `download` method. Allowing you to quickly download files from the telegram server.

Example Usage:
```python
# filtering messages with document and a file name
@bot.event("message", filters=[sub_keys("document", "file_name")])
async def on_document_message(msg: dict[str]):
    doc = msg["document"]
    file_obj = await bot("getFile", {"file_id": doc["file_id"]})
    file_path = await bot.download(file_obj, Path.cwd() / ".tmp", doc["file_name"], overwrite_existing=True)
```

## Expandability

Since this library comes without the bloat and is made for users very familiar to the Telegram Bot API, this is not a very userfriendly bot.  

It's very easy to make a user friendlier bot, using this bot as base.

Eg.
```python
from swisscore_tba_lite.core.base_bot import BaseBot, api_method_wrapper

# Make a user friendly class representing a Message
class Message:
    def __init__(self, message_id: int, ...):
        ...

# Make a class inheriting from `BaseBot` to add user frendlier methods
class Bot(BaseBot):
    @api_method_wrapper(
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

## Tasks

*Details will be added later*

## Events

*Details will be added later*

## Flexible Filter Composition System

*Details will be added later*

## Event Handler Chaining

It's possible to chain event handlers without manual re-dispatching logic by just using `return bot.event.UNHANDLED` in an event handler.

### Why is this great?

* **Graceful fallbacks:** You can write a series of specific handlers followed by a general catch-all without filter spaghetti.
* **More expressive filters:** You can "fail" a match manually even if the filters pass, which is great for edge cases (like optional preconditions).

Example Usage:
```python

from swisscore_tba_lite.filters import sub_keys

@bot.event("message", filters=[sub_keys("document", "mime_type")]]):
async def handle_pdf(msg):
    if msg["document"]["mime_type"] != "application/pdf":
        return bot.event.UNHANDLED
    
    ... # Handle pdf document

@bot.event("message", filters=[sub_keys("document", "mime_type")]]):
async def handle_file(msg):
    ... # Handle any other kind of document with a mime_type
```


