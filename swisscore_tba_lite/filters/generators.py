import re
import typing as t

from .helpers import JsonDict, false_on_key_error

def keys(*keys: str):
    """
    Generates a filter that checks for matching `keys`.  
    
    The filter returns `True` if **any** of `keys` is in `obj.keys()`
    """
    def f(obj: JsonDict):
        return any(k in obj for k in keys)
    return f

def all_keys(*keys: str):
    """
    Generates a filter that checks for matching `keys`.  
    
    The filter returns `True` if **all** of `keys` are in `obj.keys()`
    """
    def f(obj: JsonDict):
        return all(k in obj for k in keys)
    return f


def sub_keys(*key_sequence: str):
    """
    Generates a filter that checks if `key_sequence` is recursively found in obj.

    Eg. 
    ```python
    # checks if obj has key "chat" and obj["chat"] has key "is_forum"
    is_forum = sub_keys("chat", "is_forum")
    
    # checks if obj has key "from" and obj["from"] has key "is_premium"
    is_premium_user = sub_keys("from", "is_premium")
    
    # checks if obj has key "reply_to_message" 
    #   and obj["reply_to_message"] has key "photo" 
    #   and obj["reply_to_message"]["photo"] has key "caption"
    is_reply_to_photo_with_caption = sub_keys("reply_to_message", "photo", "caption")
    
    ```
    
    **Note:** The filter only checks for the **presence** of the `key_sequence` in `obj`. **Not** for their value.  
    So its perfect to check for flags which are always `True` if present. like 'is_premium' in user or 'is_forum' in chat.

    """
    def f(obj: JsonDict):
        o = obj
        for k in key_sequence:
            if isinstance(o, dict) and k in o:
                o = o[k]
                continue
            return False
        return True
    return f


def regex(*patterns: str, caption: bool = False):
    """
    Generates a filter that checks if any pattern of regular expression `patterns` matches the object text or caption.  
    
    The filter returns `True` if the regex pattern is found in obj["text"] or obj["caption"] (if `caption=True`).
    """
    pattern = re.compile("|".join(patterns))
    def f(obj: JsonDict):
        text = obj.get("text", "") if not caption else obj.get("caption", "")
        return bool(pattern.search(text))
    return f


def text_startswith(*substrings, caption: bool = False):
    def f(obj: JsonDict):
        text: str = obj.get("text", "") if not caption else obj.get("caption", "")
        return any(text.startswith(s) for s in substrings)
    return f


def commands(*commands: str, prefix: str = "/", caption: bool = False):
    """
    Generates a filter that checks for matching `commands`.  
    
    The filter returns `True` if obj["text"] starts with any "\\<prefix\\>\\<command\\>" for \\<command\\> in `commands`  
    
    Example:
    ```python
    # check for "/test" in obj["text"]
    f = commands("test", prefix="/")    
    f({"text": "test"})         # False. obj["text"] does not start with "/test"
    f({"text": "/test"})        # True.  obj["text"] starts with "/test" 
    f({"text": "/test 123"})    # True.  obj["text"] starts with "/test"
    f({"text": "/test123"})     # False. obj["text"] starts with "/test", but "/test" is not a whole word in the string.
    ```
    
    """
    commands = [rf"{prefix}{c.lstrip(prefix)}\b" for c in commands]
    return regex(*commands, caption=caption)

def chat_ids(*chat_ids: int):
    """
    Generates a filter that checks for matching `chat_ids`.
    
    The filter returns `True` if obj["chat"]["id"] is in `chat_ids`
    """
    def f(obj: JsonDict):
        return obj.get("chat", {}).get("id") in chat_ids
    return f

def chat_types(*chat_types: t.Literal["private", "group", "supergroup", "channel"]):
    """
    Generates a filter that checks for matching `chat_types`.  
    
    Valid chat types are:  
    * "private"
    * "group"
    * "supergroup"
    * "channel"
    
    The filter returns `True` if obj["chat"]["type"] is in `chat_types`
    """
    def f(obj: JsonDict):
        chat_type = obj.get("chat", {}).get("type")
        return chat_type in chat_types
    return f

def from_users(*user_ids: int):
    """
    Generates a filter that checks for matching `user_ids`.  
    
    The filter returns `True` if obj["from"]["id"] is in `user_ids`
    """
    def f(obj: JsonDict):
        from_id = obj.get("from", {}).get("id")
        return from_id in user_ids
    return f

def callback_data(*data: str):
    """
    This filter generator is meant to use for `callback_query` updates.
    
    Generates a filter that checks for matching `data`.  
    
    The filter returns `True` if obj["data"] is in `data`
    """
    def f(obj: JsonDict):
        cb_data = obj.get("data", "")
        return cb_data in data
    return f

def callback_data_startswith(*substrings: str):
    """
    This filter generator is meant to use for `callback_query` updates.
    
    Generates a filter that checks if `data` startswith any of the provided substrings.  
    
    The filter returns `True` if obj["data"] startswith any of the provided substrings
    """
    def f(obj: JsonDict):
        cb_data: str = obj.get("data", "")
        return any(cb_data.startswith(s) for s in substrings)
    return f

