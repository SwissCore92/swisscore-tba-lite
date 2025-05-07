# **SwissCore TBA Lite**

![Python](https://img.shields.io/badge/Python-3.11+-2CA5E0?style=for-the-badge&logo=python&logoColor=white)
![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-v9.0-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
<!-- ![PyPI](https://img.shields.io/badge/PyPI-1.0.0-2CA5E0?style=for-the-badge&logo=pypi&logoColor=white) -->


A minimal, async-native **Telegram Bot API** library — built for developers who want power without the clutter.

## Table of contents
* [Philosophy](#philosophy)
* [Installation](#installation)
* [Quick Start](#quick-start)
* [Automatic file processing](#automatic-file-processing)
* [Tasks](#tasks)
* [Events](#events)
* [Filters](#filters)
* [Event Handler Chaining](#event-hanlder-chaining)
* [Temporary Events](#temporary-events)
  
## Philosophy
swisscore-tba-lite is built on a simple principle: a Telegram bot library shouldn't get in your way.

Most frameworks become bloated with excessive abstractions, rigid class hierarchies, and a tangle of utility functions. But do you really need all that just to move some payloads around?

This library takes a different path.

Instead of complex abstractions, it uses plain Python `dicts`. Telegram objects are defined as `TypedDict`s—giving you full type checking and autocompletion in your editor, without incurring the overhead of runtime object creation.

Telegram methods are exposed as class methods, with required parameters as positional arguments and optional ones as keyword-only. This keeps your calls explicit, readable, and editor-friendly.

This design ensures:

* Type safety and autocompletion thanks to TypedDicts and explicit signatures
* Clean separation of required and optional parameters
* Minimal overhead, since no runtime object wrapping is involved

### One `__call__` to rule them all
Every API method is pipelined to `bot.__call__` and returns a [Task](#tasks).

```python
bot.send_message(1234, "Hello, world!")
```
is equivalent to
```python
bot("sendMessage", {
    "chat_id": 1234,
    "text": "Hello, world!"
})
```
This lets you use new Telegram Bot API methods immediately, even if the library hasn’t added the method yet. If it’s in the official Telegram docs, you can call it directly.

### Filters that feel like writing logic, not wrangling syntax
In *swisscore-tba-lite*, filtering updates is as natural as thinking in conditions. No black box magic, no custom DSLs, no endless nesting of objects. Just simple, readable functions that behave exactly like you'd expect. 

Want to check if a message is from a specific chat type, starts with a certain command, or is replying to a photo? It's as easy as calling `chat_types("supergroup")`, `commands("start")`, or `sub_keys("reply_to_message", "photo")`. You can even build complex logic using composition helpers like `if_any()`, `if_all()`, `in_not()`, or `if_none()` — pure Python, clean and powerful. The filter system is built to feel intuitive, flexible, and extendable. It's designed for developers who think in logic, not in libraries.

*See [Filtes](#filters) for more info.*

### Clear, helpful logs with privacy in mind
*swisscore_tba_lite* includes a built-in logger with optional color support (via *colorama*) to keep your terminal output clean and readable.

It gives you full visibility into what's happening under the hood, without exposing sensitive info. API tokens or payloads are never logged.

## Installation
> ⚠️ **Note:** *This library is in heavy development and not yet production-ready.*  
> * *A production ready release will follow as soon as possible.*
> * *The documentation will be improved over time.*

*Requires Python 3.11+*

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
    bot.send_message(ADMIN_ID, "Hi, I was just started!")

@bot.event("message", chat_types("private"), commands("myid"))
async def on_cmd_myid(msg: dict[str]):
    """
    Runs when a user sends '/myid' in a private chat with the bot.  
    Sends the user's ID back to them.
    """
    user_id = msg["from"]["id"]
    bot.send_message(user_id, f"Your user ID is `{user_id}`", parse_mode="Markdown")

@bot.event("message", chat_types("private"))
async def echo_message(msg: dict[str]):
    """
    Runs on any other message in a private chat with the bot.  
    Sends the same message back to the user.
    """
    bot.copy_message(msg["chat"]["id"], msg["chat"]["id"], msg["message_id"])

@bot.event("shutdown")
async def on_shutdown(exit_code: int):
    """
    Runs when the bot shuts down.  
    Sends a message to the admin indicating the bot has stopped.
    """
    if exit_code == 0:
        bot.send_message(ADMIN_ID, "Bye, I was just shut down!")

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

You can also use a `dict` with the signature ``{"content": <str, path, bytes>, "filename": <str>}``
This is useful if you:
* send files as bytes but want to preserve the filename
* want to send the file with a different name

Of course you can still just pass a valid telegram file_id or file url to send files.

<details>
<summary>Sending Files</summary>

```python
# send as str Path
photo = "path/to/your/photo1.png"
bot.send_photo(msg["chat"]["id"], photo)

# send as pathlib Path
photo = Path(photo)
bot.send_photo(msg["chat"]["id"], photo)

# send as bytes
with photo.open("rb") as f:
    photo = f.read()
bot.send_photo(msg["chat"]["id"], photo)

# send as inputfile (dict) {"content": <str, path, bytes>, "filename": <str>}
# this is useful when sending files as bytes but want to preserve the filename
#   or if you want to send the file with a different name
bot.send_photo(msg["chat"]["id"], {"content": photo, "filename": "my_photo.png"})
```

</details>

The built-in `download` method allows you to quickly download files from the telegram server. Just don't forget to fetch the file first using the `getFile` API call.

**There are some different ways to download a the file** see example below.

<details>
<summary>Downloading Files</summary>

```python
@bot.event("message", chat_ids(ADMIN_ID), is_document)
async def test(msg: tg.Message):
    doc = msg["document"]

    file = await bot.get_file(doc["file_id"])

    # download as file 
    #   if the path is a directory the file name will be taken as it is on the server
    #   else the provided filename will be used.
    #   you can optionaly allow/dissallow overwriting if the file name already exists
    path = await bot.download(file).as_file("path/to/save/file", overwrite=False)

    # download as bytes
    file_content = await bot.download(file).as_bytes()

    # download as base64 (bytes or str)
    #   as base64 bytes
    b64_bytes = await bot.download(file).as_base64()
    #   as base64 string
    b64_str = await bot.download(file).as_base64("utf-8")
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

> **Note:** The maximum number of cuncurrent request tasks can be set by `bot = Bot(..., max_concurrent_requests=<limit>)`. Default is 50.  

<details>
<summary>Example</summary>

```python
# `t` is a Task
t = bot.send_message(1234, "hello world!")

# await the task to get the result
result = await t

# or in short
result = await bot.send_message(1234, "hello world!")

# or just fire and forget
bot.send_message(1234, result["message_id"])

# Run multiple tasks in parallel (faster than awaiting individually)
# Note: they might complete in any order
results = await asyncio.gather(
    await bot.send_message(1234, "hello world!"),
    await bot.send_message(4321, "hello world!"),
    await bot.send_message(3421, "hello world!")
)
```

</details>

## Events
Every [Update](https://core.telegram.org/bots/api#update) received from Telegram is treated as an event.
The event type is derived from the update content — for example, an update with a `message` becomes a `"message"` event.

You register event handlers using `@bot.event("<event_type>")`, with optional [filters](#filters) to narrow down when the handler should trigger.

The event's object (eg.a `message`) is passed to your handler as a `dict` (a deep copy of the original object).

Important:
* Handlers **must** be async functions.
* Handlers checked in the order they were registered.
* If a handler is called, the event is considered handled and will not propagate to other handlers — unless you return `bot.event.UNHANDLED`. *See [Event Handler Chaining](#event-handler-chaining) for more info.*
* Temporary event handlers can be registered at runtime. *See [Temporary Events](#temporary-events) for more info.*

> **Note:** The maximum number of cuncurrent running event handlers can be set by `bot = Bot(..., max_concurrent_handlers=<limit>)`. Default is 8. 

<details>
<summary>Register Event Handlers</summary>

```python
from swisscore-tba-lite.filters import chat_types, is_text, is_photo

@bot.event("message", chat_types("private"), is_text)
async def on_private_message(msg: dict):
    ... #Will run if a text message in a private chat is received

@bot.event("message", chat_types("supergroup"), is_photo)
async def on_supergroup_message(msg: dict):
    ... #Will run if a photo message in a supergroup chat is received

...

```

</details>

## Filters
Each event handler can use an optional list of filters — functions with the signature `(obj: dict) -> bool`.
All filters must return truthy values for the event to pass.

Filters can be regular or async functions. You can write your own, use `lambda`s or use the handy helpers in `swisscore_tba_lite.filters`.

It includes:
* Filter generators
* Preconfigured filters
* Composables like `if_not()`, `if_any()`, `if_all()`, and `if_none()` — giving you *powerful* but **readable** logic for handler conditions.

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

@bot.event("message", is_my_chat, commands("settings"))
async def on_cmd_settings(msg: dict):
    # runs only if YOU use the /settings command 
    # in private chat with the bot
    ...
```

</details>


You can also define your own filters.

## Event Handler Chaining
It's possible to chain event handlers without manual re-dispatching logic by just using `return bot.event.UNHANDLED` in an event handler.

***Why is this great?***
* **Graceful fallbacks:** You can write a series of specific handlers followed by a general catch-all without filter spaghetti.
* **More expressive filters:** You can "fail" a match manually even if the filters pass, which is great for edge cases (like optional preconditions).

You can also turn an event handler into a filter.

```python
ADMIN_ID = int(os.environ.get("ADMIN_ID", 1234))

unauthorized_chat = if_not(chat_ids(ADMIN_ID))

@bot.event("message", unauthorized_chat)
async def on_unouthorized_chat(_):
    ... # ignore 

# this message event handler section will only be reached by the admin

@bot.event("message", ...)
async def on_msg(msg): ...

@bot.event("message", ...)
async def on_msg(msg): ...

@bot.event("message", ...)
async def on_msg(msg): ...

```

See [Temporary Events](#temporary-events) for more usecases of `bot.event.UNHANDLED`.

<details>
<summary>Example</summary>

```python

from swisscore_tba_lite.filters import sub_keys

@bot.event("message", sub_keys("document", "mime_type"))
async def handle_pdf(msg):
    if msg["document"]["mime_type"] != "application/pdf":
        return bot.event.UNHANDLED
    
    ... # Handle pdf document

@bot.event("message", sub_keys("document", "mime_type"))
async def handle_file(msg):
    ... # Handle any other kind of document with a mime_type
```

</details>

## Temporary Events

This library allows you to **register temporary event handlers** at runtime `using bot.event.wait_for(...)`. These handlers are useful for managing dynamic, stateful conversation flows—such as wizards, confirmation dialogs, or guided inputs—where user interaction drives the next steps. 
 
Temporary event handlers are short-lived and are **not persisted across bot restarts**. They are best suited for ephemeral, in-session workflows where you want to "wait" for a specific user input before proceeding.

***How it works***
* Temporary event handlers are registered dynamically using `bot.event.wait_for(...)`.
* They are context-aware, meaning you can pass and maintain custom state (via a arbitrary context object) between steps.
* They operate on a first-matched, first-handled basis and can be layered to form multi-step flows.
* If a temporary event handler matches, the event vill **will not** propagate to static/default event handlers. No matter if `bot.event.UNHANDLED` was returned.
* If a temporary event handler returns `bot.event.UNHANDLED`, the temporary event handler will be considered unhandled and will continue listening for future matching events (updates). **Else, it will be removed automatically**.

*Note: Temporary event handlers exist only in memory. They are lost on bot restart.*

<details>
<summary>Example</summary>

```python
# define a test command handler
@bot.event("message", chat_types("private"), commands("test"))
async def test_cmd(msg: tg.Message):
    # define a temporary handler
    async def countdown(m: tg.Message, ctx: dict):
        if ctx["count"] > 0:
            bot("sendMessage", {
                "chat_id": m["chat"]["id"],
                "text": f"Explode after {ctx["count"]}..."
            })
            ctx["count"] -= 1
            return bot.event.UNHANDLED
        
        bot.send_message(msg["chat"]["id"], "BOOM! 💥")
    
    # define a temporary canel command handler
    async def cancel_countdown(msg: dict):
        bot.send_message(msg["chat"]["id"], "Explosion canceled!")
    
    context = {"count": 3}
    await countdown(msg, context)

    # register the temporary handler
    bot.event.wait_for("message", chat_ids(msg["chat"]["id"]), 
        handlers=[
            (cancel_countdown, [commands("cancel")]),
            (countdown, []),
        ], 
        context=context
    )
```

</details>

<details>
<summary>Advanced Example</summary>

```python
# Mimic @BotFather's /setuserpic command #

# define a /cancel command event handler with an optional context argument
@bot.event("message", chat_types("private"), commands("cancel"))
async def on_cmd_cancel(msg: tg.Message, ctx: dict | None = None):
    if ctx:
        # context was passed, so tell the user that the action was cancelled
        bot.send_message(
            msg["chat"]["id"], 
            f"The command {ctx["action"]} has been cancelled. Anything else I can do for you?",
            reply_markup={"remove_keyboard": True}
        )
        # return nothing, so the temporary event is considered handled (finished)
        return

    # no context was passed, so there is nothing to cancel
    bot.send_message(msg["chat"]["id"], "No active command to cancel. I wasn't doing anything anyway. Zzzzz...😴")


# define a /setuserpic command event handler 
@bot.event("message", chat_types("private"), commands("setuserpic"))
async def on_cmd_set_pic(msg: tg.Message):

    # define a filter to make sure to target the correct chat and user 
    is_valid_chat_user = if_all(
        chat_ids(msg["chat"]["id"]), 
        from_ids(msg["from"]["id"])
    )

    # define an temporary event handler to check if the user has sent a valid photo 
    # accept the context as second argument which contains the chosen bot's name
    async def set_bot_pic(msg: tg.Message, ctx: dict):
        if msg.get("photo"):
            # the user has sent a valid photo
            bot.send_message(msg["chat"]["id"], f"Success! Profile photo of {ctx["bot_name"]} updated.")

            # return nothing, so the temporary event is considered handled (finished)
            return
        
        if msg.get("document"):
            # the user has sent a file instead of a photo
            bot.send_message(msg["chat"]["id"], "Please send me the picture as a 'Photo', not as a 'File'.")

            # return bot.event.UNHANDLED, so the temporary event is considered unhandled and continues
            return bot.event.UNHANDLED
        
        # the user has sent something other than a file or a photo
        bot.send_message(msg["chat"]["id"], "I said send me a <b>photo</b>. Not some other nonesense.", parse_mode="HTML")

        # return bot.event.UNHANDLED, so the temporary event is considered unhandled and continues
        return bot.event.UNHANDLED
    
    # define an temporary event handler to check if the user provided a valid bot name
    # accept the context as second argument which contains a list of valid bot names
    async def check_selected_bot(msg: tg.Message, ctx: dict):

        bot_name = msg.get("text", "").strip()
        if bot_name in ctx["valid_bots"]:
            # the provided bot name was valid 
            bot.send_message(msg["chat"]["id"], "OK. Send me the new profile photo for the bot.", reply_markup={"remove_keyboard": True})

            # register the next step of the temporary event to check for a valid bot picture
            bot.event.wait_for("message", is_valid_chat_user,
                handlers=[
                    (on_cmd_cancel, [commands("cancel")]), 
                    (set_bot_pic, [])
                ], 
                context={"action": "setuserpic", "bot_name": bot_name}
            )

            # return nothing, so this step of the temporary event is considered handled (finished)
            # but we already registered the next step above
            return
        
        # the user didn't provide a valid bot name
        bot.send_message(msg["chat"]["id"], "Invalid bot selected. Please send a valid bot name.")

        # return bot.event.UNHANDLED, so the temporary event is considered unhandled and continues
        return bot.event.UNHANDLED

    # define a fake bot list for the user to choose from
    bots = ["@my_cool_bot1", "@my_cool_bot2", "@my_coolest_bot3"]

    # send a message with a reply keyboard for the user to choose a bot
    bot.send_message(
        msg["chat"]["id"],
        "Choose a bot to change profile photo.",
        reply_markup={
            "keyboard": [[{"text": bot_name}] for bot_name in bots],
            "one_time_keyboard": True,
            "resize_keyboard": True,
            "input_field_placeholder": "Enter the bot's username"
        },
    )

    # register the first step of the temporary event to check for a valid bot name
    bot.event.wait_for("message", is_valid_chat_user,
        handlers=[
            (on_cmd_cancel, [commands("cancel")]),
            (check_selected_bot, [])
        ], 
        context={"action": "setuserpic", "valid_bots": bots}
    )
```

</details>


**That's all i got for now**, more will follow.
