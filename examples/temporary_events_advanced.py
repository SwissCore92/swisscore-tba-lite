import os 

from swisscore_tba_lite import Bot
from swisscore_tba_lite import objects as tg
from swisscore_tba_lite.filters import commands, chat_types, chat_ids, from_ids, if_all

bot = Bot(os.environ.get("API_TOKEN", "<YOUR_API_TOKEN>"))


# Mimic @BotFather's /setuserpic command 


# define a startup event handler
@bot.event("startup")
async def on_startup():
    # Set the bots commands for private chats
    # Note: you may have to close and reopen the chat with your bot to see these changes
    bot.set_my_commands([
        {"command": "setuserpic", "description": "change bot profile photo"},
        {"command": "cancel", "description": "cancel the current operation"}
    ], scope={"type": "all_private_chats"})


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

# define a shutdown event handler
@bot.event("shutdown")
async def on_shutdown(_):
    # remove the bots commands for private chats
    # Note: you may have to close and reopen the chat with your bot to see these changes
    bot.delete_my_commands(scope={"type": "all_private_chats"})


# start the bot in polling mode
bot.start_polling()
