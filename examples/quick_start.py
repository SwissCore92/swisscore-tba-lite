import os 

from swisscore_tba_lite import Bot
from swisscore_tba_lite import objects as tg
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
async def on_cmd_myid(msg: tg.Message):
    """
    Runs when a user sends '/myid' in a private chat with the bot.  
    Sends the user's ID back to them.
    """
    user_id = msg["from"]["id"]
    bot.send_message(user_id, f"Your user ID is `{user_id}`", parse_mode="Markdown")

@bot.event("message", chat_types("private"))
async def echo_message(msg: tg.Message):
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
