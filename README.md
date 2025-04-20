# **SwissCore TBA Lite**
![Python](https://img.shields.io/badge/python-3.11%2B-blue)  

A minimal, async-native **Telegram Bot API** library — built for developers who want power without the clutter.

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
* [Temporary Events](#temporary-events)
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

*See [Tasks](#tasks) for more info.*

### Always Up-to-Date with *Telegram Bot API*
One of the biggest frustrations with traditional libraries is lag — you find a new feature in the [*Telegram Bot API docs*](https://core.telegram.org/bots/api), but your library doesn’t support it yet. With *swisscore-tba-lite*, that's a thing of the past.  

The core design guarantees that every method and every parameter supported by the official API is instantly usable — no waiting for a new release, no patching, no forking. If it’s in the *Telegram Bot API docs*, you can use it right now. Just pass the method name and your params and let the magic happen.

### Minimal by default, extensible by design
At its core, *swisscore-tba-lite* is lean and async-native. You only get the essentials: fast event handling, decorators that feel natural, and a clean internal event loop with graceful shutdown support.

But if you want more? Build it on top. This is your foundation — not your cage.

*See [Expandability](#expandability) for more info.*

### Built for reliability and control
This library is designed with predictability in mind. Startup and shutdown sequences are clean and observable. Handlers are just async functions. And whether you’re running your bot in sync application like flask or an async application like an aiohttp web app, it plugs in without drama. 

*See [Runners](#runners) for more info.*

### Filters that feel like writing logic, not wrangling syntax
In *swisscore-tba-lite*, filtering updates is as natural as thinking in conditions. No black box magic, no custom DSLs, no endless nesting of objects. Just simple, readable functions that behave exactly like you'd expect. 

Want to check if a message is from a specific chat type, starts with a certain command, or is replying to a photo? It's as easy as calling `chat_types("supergroup")`, `commands("start")`, or `sub_keys("reply_to_message", "photo")`. You can even build complex logic using composition helpers like `any_()`, `all_()`, `not_()`, or `none_()` — pure Python, clean and powerful. The filter system is built to feel intuitive, flexible, and extendable. It's designed for developers who think in logic, not in libraries.

*See [Filtes](#filters) for more info.*

### Clear, helpful logs with privacy in mind
*swisscore_tba_lite* includes a built-in logger with optional color support (via *colorama*) to keep your terminal output clean and readable.

It gives you full visibility into what's happening under the hood, without exposing sensitive info. API tokens, file contents, local file paths and payloads are never logged. You always stay informed, without compromising user privacy.

## Installation
> ⚠️ **Note:** *This library is in heavy development and not yet production-ready.*  
> * *A production ready release will follow as soon as possible.*
> * *The documentation will be improved over time.*

*Requires Python 3.11+*

*It's recommended to use a virtual environment*

Since there is no PyPI release at the moment, you have to install it from source using `pip` & `git`.

```sh
pip install git+https://github.com/SwissCore92/swisscore-tba-lite.git
```
*Note: On Linux/MacOS you may have to use `pip3`*.

## Quick Start
```python
import os 

from swisscore_tba_lite import Bot
from swisscore_tba_lite.filters import commands, chat_types

# Get your Telegram Bot API Token from @BotFather
# Set it in an environment variable (API_TOKEN) or manually replace <YOUR_API_TOKEN> below
TOKEN = os.environ.get("API_TOKEN", "<YOUR_API_TOKEN>")

# Optional:
# Get your Telegram user ID
# (You can use the `/myid` command below in private chat with your bot if you don't know it)
# Set it in an environment variable (ADMIN_ID) or manually replace 1234 below
ADMIN_ID = int(os.environ.get("ADMIN_ID", 1234))

bot = Bot(TOKEN)

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

@bot.event("message", filters=[chat_types("private")])
async def echo_message(msg: dict[str]):
    """
    Runs on any other message in a private chat with the bot.  
    Sends the same message back to the user.
    """
    bot("copyMessage", {
        "from_chat_id": msg["chat"]["id"],
        "chat_id": msg["chat"]["id"],
        "message_id": msg["message_id"]
    })

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
Simple things like file handling are taken care of automatically.
For example, fields like `InputFile` or the media field in `InputMedia` and `InputPaidMedia` can be:
* a `str` (path to the file),
* a `pathlib.Path`, or
* raw `bytes`.

The bot will handle everything under the hood — as long as `check_input_files` or `check_input_media` are properly enabled.

Of course you can still just pass a valid telegram file_id or file url to send files.

<details>
<summary>Sending Files</summary>

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

</details>

The built-in `download` method allows you to quickly download files from the telegram server. Just don't forget to fetch the file first using the `getFile` API call.

<details>
<summary>Downloading Files</summary>

```python
# filtering messages with document and a file name
@bot.event("message", filters=[sub_keys("document", "file_name")])
async def on_document_message(msg: dict[str]):
    doc = msg["document"]
    file_obj = await bot("getFile", {"file_id": doc["file_id"]})
    file_path = await bot.download(file_obj, Path.cwd() / ".tmp", doc["file_name"], overwrite_existing=True)
```

</details>

## Expandability
This library is intentionally minimal and made for developers already familiar with the Telegram Bot API — so it's not designed to be overly user-friendly out of the box.

But that's a feature, not a bug: it gives you full control.
Creating your own abstractions and user-friendly wrappers on top of this core is simple and clean.

<details>
<summary>Example</summary>
 
```python
from swisscore_tba_lite.core.base_bot import BaseBot, api_method_wrapper

# Custom class to wrap Telegram messages
class Message:
    def __init__(self, message_id: int, ...):
        ...

# Extend the BaseBot with your own high-level methods
class Bot(BaseBot):
    @api_method_wrapper(
        check_input_files=["photo"], 
        convert_func=lambda m: Message(**m)
    )
    def send_photo(chat_id: int, photo: str | Path | bytes, ...) -> asyncio.Task[Message]:
        """
        No implementation needed — the decorator handles everything.

        - Method name is auto-converted to camelCase.
        - If `photo` is a path, Path object, or bytes, 
          it will be uploaded automatically.
        - File IDs and URLs are still supported as plain strings.
        - `convert_func` wraps the result into a Message instance,
          but you can use any conversion logic you prefer.
        """

bot = Bot("<YOUR_TOKEN>")

@bot.event("startup")
async def startup()
    msg = await bot.send_photo(...)

bot.start_polling()
```

</details>

## Tasks
Every call to a bot method returns an `asyncio.Task`.
You can either `await` it to get the result, or just fire it and forget it — *your choice*.

***Why Tasks instead of regular coroutines?***  
Because it's **faster**, more **flexible**, and a perfect fit for scenarios like this where most of the time is spent waiting on server responses.

By using tasks:
* You avoid blocking your event handlers.
* You can schedule multiple API calls simultaneously.
* You only wait for results when you actually need them.

This allows your bot to stay snappy and responsive, even during heavy workloads.

> **Note:** The maximum number of cuncurrent tasks can be set by `bot.max_concurrent_tasks = <limit>`.  
> If the limit is exceeded, the bot will automatically gather all pending tasks before it continues processing updates.  
> Default is *50*.

<details>
<summary>Example</summary>

```python
# `t` is a Task
t = bot("sendMessage", {
    "chat_id": 1234, 
    "text": "hello world!"
})

# await the task to get the result
result = await t

# or in short
result = await bot("sendMessage", {
    "chat_id": 1234, 
    "text": "hello world!"
})

# or just fire and forget
bot("deleteMessage", {
    "chat_id": result["chat"]["id"], 
    "message_id": result["message_id"]
})

# Run multiple tasks in parallel (faster than awaiting individually)
# Note: they might complete in any order
results = await asyncio.gather(
    bot("sendMessage", {"chat_id": 1234, "text": "hello world!"}),
    bot("sendMessage", {"chat_id": 4321, "text": "hello world!"}),
    bot("sendMessage", {"chat_id": 3412, "text": "hello world!"})
)
```

</details>

## Events
Every [Update](https://core.telegram.org/bots/api#update) received from Telegram is treated as an event.
The event type is derived from the update content — for example, an update with a `message` becomes a `"message"` event.

You register event handlers using `@bot.event("<event_type>")`, with optional [filters](#filters) to narrow down when the handler should trigger.

The event's object (eg.a `message`) is passed to your handler as a `dict`.

Important:
* Handlers **must** be async functions.
* Handlers run in the order they were registered.
* If a handler is called, the event is considered handled and will not propagate to other handlers — unless you return `bot.event.UNHANDLED`. *See [Event Handler Chaining](#event-handler-chaining) for more info.*
* Temporary event handlers can be registered at runtime. *See [Temporary Events](#temporary-events) for more info.*

<details>
<summary>Example</summary>

```python
from swisscore-tba-lite.filters import chat_types, is_text, is_photo

@bot.event("message", filters=[chat_types("private"), is_text])
async def on_private_message(msg: dict):
    ... #Will run if a text message in a private chat is received

@bot.event("message", filters=[chat_types("supergroup"), is_photo])
async def on_supergroup_message(msg: dict):
    ... #Will run if a photo message in a supergroup chat is received

... # define more filters

```

</details>

## Filters
Each event handler can use an optional list of filters — functions with the signature `(obj: dict) -> bool`.
All filters must return truthy values for the event to pass.

Filters can be regular or async functions. You can write your own, use `lambda`s or use the handy helpers in `swisscore_tba_lite.filters`.

It includes:
* Filter generators
* Preconfigured filters
* Composables like `not_()`, `any_()`, `all_()`, and `none_()` — giving you *powerful* but **readable** logic for handler conditions.

Everything is well-documented and easy to use.

<details>
<summary>Simple filter usage</summary>

```python
from swisscore-tba-lite.filters import (
    chat_ids,
    user_ids, 
    commands
)

is_my_chat = chat_ids(<your_user_id>)
is_me = user_ids(<your_user_id>)

@bot.event("message", filters=[is_my_chat, commands("settings")])
async def on_cmd_settings(msg: dict):
    # runs only if YOU use the /settings command 
    # in private chat with the bot
    ...
```

</details>

<details>
<summary>Defining your own filters (or generators)</summary>

```python
from swisscore_tba_lite.filters import (
    chat_types, 
    commands,
    false_on_key_error
)

# define a filter generator for easy reuse
async def has_permission(permission: str):
    """
    check if both (performer **and** bot) have the required `permission` to perform a specific action. 
    """

    # define the filter 
    @false_on_key_error
    async def f(msg: dict):

        # get a list of all chat administrators (excluding other bots)
        admins = await bot("getChatAdministrators", {
            "chat_id": msg["chat"]["id"]
        })

        # create an admin dict {user_id: ChatMember}
        admin_dict = {member["user"]["id"]: member for member in admins}

        # check if the user is an admin
        if not msg["from"]["id"] in admin_dict:
            # the user is not an admin
            return False

        # check if the bot is an admin
        if not bot.user_id in admin_dict:
            # the bot is not an admin. 
            # the action can not be performed by the bot anyway
            return False
        
        # extract the admin from admin dict
        admin = admin_dict[msg["from"]["id"]]
        
        # check if the admin has the required permission ("creator" always has all permissions)
        if not (admin["status"] == "creator" or admin[permission]):
            # the admin does not have the required permission 
            return False
        
        # check if the bot has the required permission
        if not admin_dict[bot.user_id][permission]:
            # the bot does not have the required permission 
            return False
        
        # both (user and bot) are admins with the required permission :)
        return True
    
    # return the filter
    return f


@bot.event("message", filters=[
    chat_types("supergroup"), 
    commands("ban"), 
    has_permission("can_restrict_members")
])
async def ban_chat_member(msg: dict):
    # runs only if the performer and the bot are both chat administrators
    # with the `can_restrict_members` permission.
    bot("banChatMember", {...})


@bot.event("message", filters=[
    chat_types("supergroup"), 
    commands("promote"), 
    has_permission("can_promote_members")
])
async def promote_chat_member(msg: dict):
    # runs only if the performer and the bot are both chat administrators
    # with the `can_promote_members` permission. 
    bot("promoteChatMember", {...})

```

</details>  

## Event Handler Chaining
It's possible to chain event handlers without manual re-dispatching logic by just using `return bot.event.UNHANDLED` in an event handler.

***Why is this great?***
* **Graceful fallbacks:** You can write a series of specific handlers followed by a general catch-all without filter spaghetti.
* **More expressive filters:** You can "fail" a match manually even if the filters pass, which is great for edge cases (like optional preconditions).

<details>
<summary>Example</summary>

But where `bot.event.UNHANDLED` really shines is in [Temporary Events](#temporary-events).

```python

from swisscore_tba_lite.filters import sub_keys

@bot.event("message", filters=[sub_keys("document", "mime_type")])
async def handle_pdf(msg):
    if msg["document"]["mime_type"] != "application/pdf":
        return bot.event.UNHANDLED
    
    ... # Handle pdf document

@bot.event("message", filters=[sub_keys("document", "mime_type")])
async def handle_file(msg):
    ... # Handle any other kind of document with a mime_type
```

</details>

## Temporary Events
*Details will be added later*

## Runners
*Details will be added later*


