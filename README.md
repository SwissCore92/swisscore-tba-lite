# **SwissCore TBA Lite**
![Python](https://img.shields.io/badge/python-3.11%2B-blue)  

A minimal, async-native Telegram Bot API library — built for developers who want power without the clutter.

## Table of contents
* [Philosophy](#philosophy)
* [Installation](#installation)
* [Quick Start](#quick-start)
* [Automatic file processing](#automatic-file-processing)
* [Expandability](#expandability)
* [Tasks](#tasks)
* [Events](#events)
* [Filters](#filters)
* [Event Handler Chaining](#event-hanlder-chaining)
* [Runners](#runners)
  
## Philosophy
*swisscore-tba-lite* is built on a simple idea: **a Telegram bot library shouldn't get in your way.**

Most bot frameworks end up bloated with layers of abstractions, rigid class hierarchies, and dozens of overlapping utility functions. You start with something small, and suddenly you're drowning in dataclasses just to send a message.

This library takes a different approach.

### One `__call__` to rule them all
Every Telegram API method is just a dictionary away. Want to call sendMessage? You just call the bot like a function:

```python
bot("sendMessage", {
    "chat_id": 1234,
    "text": "Hello, world!"
})
```

That’s it. One unified entrypoint. *Await it* or *forget it*. **It's your decision**. 

More about this topic in the [Tasks](#tasks) section.

### Always Up-to-Date with *Telegram Bot API*
One of the biggest frustrations with traditional libraries is lag — you find a new feature in the [*Telegram Bot API docs*](https://core.telegram.org/bots/api), but your library doesn’t support it yet. With *swisscore-tba-lite*, that's a thing of the past.  

The core design guarantees that every method and every parameter supported by the official API is instantly usable — no waiting for a new release, no patching, no forking. If it’s in the *Telegram Bot API docs*, you can use it right now. Just pass the method name and your params and let the magic happen.

### Minimal by default, extensible by design
At its core, *swisscore-tba-lite* is lean and async-native. You only get the essentials: fast event handling, decorators that feel natural, and a clean internal event loop with graceful shutdown support.

But if you want more? Build it on top. This is your foundation — not your cage.

More about this topic in the [Expandability](#expandability) section.

### Built for reliability and control
This library is designed with predictability in mind. Startup and shutdown sequences are clean and observable. Handlers are just async functions. And whether you’re running a threaded Flask app or an aiohttp webhook server, it plugs in without drama. 

More about this topic in the [Runners](#runners) section.

### Filters that feel like writing logic, not wrangling syntax
In *swisscore-tba-lite*, filtering updates is as natural as thinking in conditions. No black box magic, no custom DSLs, no endless nesting of objects. Just simple, readable functions that behave exactly like you'd expect. 

Want to check if a message is from a specific chat type, starts with a certain command, or is replying to a photo? It's as easy as calling `chat_types("supergroup")`, `commands("start")`, or `sub_keys("reply_to_message", "photo")`. You can even build complex logic using composition helpers like `any_()`, `all_()`, `not_()`, or `none_()` — pure Python, clean and powerful. The filter system is built to feel intuitive, flexible, and extendable. It's designed for developers who think in logic, not in libraries.

More about this topic in the [Filtes](#filters) section.

### Clear, helpful logs with privacy in mind
*swisscore_tba_lite* includes a built-in logger with optional color support (via *colorama*) to keep your terminal output clean and readable.

It gives you full visibility into what's happening under the hood, without exposing sensitive info. API tokens, file contents, local file paths and payloads are never logged. You always stay informed, without compromising user privacy.

## Installation
> ⚠️ **Note:** *This library is in early development and not yet production-ready.*  
> * *A production ready release will follow as soon as possible.*
> * *The documentation will be improved over time.*

<!-- ### Create and activate a virtual Environment
While this is optional, it's highly recommended to use a virtual environment to avoid conflicts with other Python projects.  
It's also a save place to store your Telegram Bot API token.

Open a Terminal in a work directory of your choice.

```sh
# Create venv
python -m venv .venv

# Activate venv (Linux/macOS)
source .venv/bin/activate

# Activate venv (Windows)
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
``` -->

### Installation
*Requires Python 3.11+*

Since there is no PyPI release at the moment, you have to install it from source using `pip` & `git`.

```sh
pip install git+https://github.com/SwissCore92/swisscore-tba-lite.git
```
*Note: On Linux/MacOS you may have to use `pip3`*.

### Editable Install (For Development)
```sh
git clone https://github.com/SwissCore92/swisscore-tba-lite.git
cd swisscore-tba-lite
pip install -e .
```
*Note: On Linux/MacOS you may have to use `pip3`*.

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
        convert_func=lambda m: Message(**m)
    )
    def send_photo(chat_id: int, photo: str | Path | bytes, ...):
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
The event system in *swisscore-tba-lite* is built to let you express logic naturally — no boilerplate, no acrobatics. You register event handlers using `@bot.event(...)`, with optional filters to fine-tune what should trigger them. 

Filters can be stacked, combined with logic helpers like any_() or and_(), and reused — making your bot code both clean and expressive. 

Handlers run in order, and if one returns bot.event.UNHANDLED, the next matching handler gets a shot — great for small, focused functions without stepping on each other’s toes. For more dynamic flows, like multi-step interactions or temporary commands, `bot.event.wait_for(...)` lets you define one-off handlers with optional filters and even attach a custom context — ideal for implementing things like confirmation prompts or user-specific flows. It’s flexible, predictable, and built for real-world use.

*More Details will be added later*

## Filters
*Details will be added later*

## Temporary Events
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

## Runners
*Details will be added later*


