import os

from swisscore_tba_lite import BaseBot as Bot
from swisscore_tba_lite.filters import commands, chat_types, chat_ids

bot = Bot(os.environ.get("API_TEST_TOKEN", "<YOUR_API_TOKEN>"))

# define a test command handler
@bot.event("message", chat_types("private"), commands("test"))
async def test_cmd(msg: dict):
    # define a temporary handler
    async def countdown(m: dict, ctx: dict):
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
    
    # define a temporary canel command handler
    async def cancel_countdown(msg: dict):
        bot("sendMessage", {
            "chat_id": msg["chat"]["id"],
            "text": "Explosion canceled!"
        })
    
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

bot.start_polling()
