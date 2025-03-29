import typing as t

from . import utils

def keys(keys: str | list[str]):
    """
    Generates a filter that checks for matching `keys`.  
    
    The filter returns `True` if any of `keys` is in `obj.keys()`
    """
    keys = utils.to_list(keys)
    def f(obj: dict[str, t.Any]):
        return any(k in obj for k in keys)
    return f

def commands(commands: str | list[str], prefix: str = "/"):
    """
    Generates a filter that checks for matching `commands`.  
    
    The filter returns `True` if obj["text"] starts with any "\\<prefix\\>\\<command\\>" for \\<command\\> in `commands`  
    Eg. if `commands` is ["start"] or "start" and prefix is "/" it checks for "/start"
    """
    commands = [f"{prefix}{c.lstrip(prefix)}" for c in utils.to_list(commands)]
    def f(obj: dict[str, t.Any]):
        return any(utils.startswith_word(obj.get("text", ""), cmd) for cmd in commands)  
    return f

def chat_types(chat_types: str | list[str]):
    """
    Generates a filter that checks for matching `chat_types`.  
    
    The filter returns `True` if obj["chat"]["type"] is in `chat_types`
    """
    chat_types = utils.to_list(chat_types)
    def f(obj: dict[str, t.Any]):
        chat_type = obj.get("chat", {}).get("type")
        return chat_type in chat_types
    return f

def from_users(user_ids: int | list[int]):
    """
    Generates a filter that checks for matching `user_ids`.  
    
    The filter returns `True` if obj["from"]["id"] is in `user_ids`
    """
    user_ids = utils.to_list(user_ids)
    def f(obj: dict[str, t.Any]):
        from_id = obj.get("from", {}).get("id")
        return from_id in user_ids
    return f

# TODO: Add much more filters