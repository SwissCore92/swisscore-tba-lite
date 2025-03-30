# **SwissCore TBA Lite**
![Python](https://img.shields.io/badge/python-3.11%2B-blue)  

A very basic and lightweight asynchronous [Telegram Bot API](https://core.telegram.org/bots/api) wrapper for **python 3.11+**.


Handles just in *dictionaries*. 

* [Installation](#installation)
* [Quick Start](#quick-start)

---

## Installation

*Requires Python 3.11+*

#### Installation on Windows  
```sh
python -m pip install git+https://github.com/SwissCore92/swisscore-tba-lite.git
```

#### Installation on Linux / MacOS   
```sh
python3 -m pip install git+https://github.com/SwissCore92/swisscore-tba-lite.git
```

---

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

bot.start_polling()

```