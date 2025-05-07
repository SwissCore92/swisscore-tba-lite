import os

from swisscore_tba_lite import Bot
from swisscore_tba_lite import objects as tg
from swisscore_tba_lite.filters import commands, chat_types, chat_ids

bot = Bot(os.environ.get("API_TEST_TOKEN", "<YOUR_API_TOKEN>"))

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

bot.start_polling()
