import os

from swisscore_tba_lite import Bot
from swisscore_tba_lite import objects as tg
from swisscore_tba_lite.filters import (
    chat_types, 
    commands,
    false_on_key_error
)

bot = Bot(os.environ.get("API_TOKEN", "<YOUR_API_TOKEN>"))

# define a filter generator for easy reuse
async def has_permission(permission: str):
    """
    check if both (performer **and** bot) have the required `permission` to perform a specific action. 
    """

    # define the filter 
    @false_on_key_error
    async def f(msg: tg.Message):

        # get a list of all chat administrators (excluding bots)
        admins = await bot.get_chat_administrators(msg["chat"]["id"])

        # create an admin dict {user_id: ChatMember} (might raise a KeyError)
        admin_dict = {member["user"]["id"]: member for member in admins}

        # check if the user is an admin
        if not msg["from"]["id"] in admin_dict:
            # the user is not an admin
            return False

        # extract the admin from admin dict
        admin = admin_dict[msg["from"]["id"]]
        
        # check if the admin has the required permission ("creator" always has all permissions)
        if admin["status"] != "creator" or not admin.get(permission):
            # the admin does not have the required permission 
            return False
        
        # get the bot as chat member
        my_member = await bot.get_chat_member(msg["chat"]["id"], bot.user_id)

        # check if the bot is an admin and has the required permission (might raise a KeyError)
        if my_member["status"] != "administrator" or not my_member.get(permission):
            # the bot is not an admin or is not permitted. 
            # the action can not be performed by the bot
            return False
        
        # both (user and bot) are admins with the required permission :)
        return True
    
    # return the filter
    return f


@bot.event("message", 
    chat_types("supergroup"), 
    commands("ban"), 
    has_permission("can_restrict_members")
)
async def ban_chat_member(msg: tg.Message):
    # runs only if the performer and the bot are both chat administrators
    # with the `can_restrict_members` permission.
    bot.ban_chat_member(msg["chat"]["id"], ...)


@bot.event("message", 
    chat_types("supergroup"), 
    commands("promote"), 
    has_permission("can_promote_members")
)
async def promote_chat_member(msg: tg.Message):
    # runs only if the performer and the bot are both chat administrators
    # with the `can_promote_members` permission. 
    bot.promote_chat_member(msg["chat"]["id"], ...)
