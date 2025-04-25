import subprocess
import os

from swisscore_tba_lite import Bot, objects as tg
from swisscore_tba_lite.filters import commands, chat_types, chat_ids, from_ids


# Get your Telegram Bot API Token from @BotFather
# Set it in an environment variable (API_TOKEN) or manually replace <YOUR_API_TOKEN> below
TOKEN = os.environ.get("API_TOKEN", "<YOUR_API_TOKEN>")

# Optional:
# Get your Telegram user ID
# (You can use the `/myid` command below in private chat with your bot if you don't know it)
# Set it in an environment variable (ADMIN_ID) or manually replace 1234 below
ADMIN_ID = int(os.environ.get("ADMIN_ID", 1234))

bot = Bot(
    TOKEN, 
    # base_api_url="http://localhost:8081", 
    # base_file_url="http://localhost:8081/file"
)

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

    
# add a test command handler
@bot.event("message", chat_types("private"), commands("test"))
async def test_cmd(msg: tg.Message):
    # define a temporary handler
    async def countdown(m: tg.Message, ctx):
        if ctx["count"] > 0:
            bot("sendMessage", {
                "chat_id": m["chat"]["id"],
                "text": f"Explode after {ctx["count"]}..."
            })
            ctx["count"] -= 1
            return bot.event.UNHANDLED
        
        bot("sendMessage", {
            "chat_id": msg["chat"]["id"],
            "text": "BOOM! 💥"
        })
    
    context = {"count": 3}
    await countdown(msg, context)

    # register the temporary handler
    bot.event.wait_for("message", [
        (countdown, [chat_ids(msg["chat"]["id"])]),
    ], context=context)

@bot.event("message", chat_types("private"), commands("myid"))
async def on_cmd_myid(msg: tg.Message):
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
