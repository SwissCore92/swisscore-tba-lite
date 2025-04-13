"""Provides some filter generators and some preconfigured filters."""

import re
import typing as t
from inspect import iscoroutinefunction

def false_on_key_error(func):
    """
    This is a decorator that returns false if a `KeyError` is raised during filter evaluation.  
    
    Can be used for both regular and coroutine functions.
    
    Ussage  
    ```python
    @false_on_key_error
    def my_filter(obj):
        # if a KeyError is raised, False is returned. 
        return obj["chat"] 
    ```
    """
    if iscoroutinefunction(func):
        async def async_wrapper(obj):
            try:
                return bool(await func(obj))
            except KeyError:
                return False
        
        return async_wrapper

    def wrapper(obj):
        try:
            return bool(func(obj))
        except KeyError:
            return False
        
    return wrapper

def keys(*keys: str):
    """
    Generates a filter that checks for matching `keys`.  
    
    The filter returns `True` if **any** of `keys` is in `obj.keys()`
    """
    def f(obj: dict[str, t.Any]):
        return any(k in obj for k in keys)
    return f

def all_keys(*keys: str):
    """
    Generates a filter that checks for matching `keys`.  
    
    The filter returns `True` if **all** of `keys` are in `obj.keys()`
    """
    def f(obj: dict[str, t.Any]):
        return all(k in obj for k in keys)
    return f

def regex(*patterns: str, caption: bool = False):
    """
    Generates a filter that checks if any pattern of regular expression `patterns` matches the object text or caption.  
    
    The filter returns `True` if the regex pattern is found in obj["text"] or obj["caption"] (if `caption=True`).
    """
    pattern = re.compile("|".join(patterns))
    def f(obj: dict[str, t.Any]):
        text = obj.get("text", "") if not caption else obj.get("caption", "")
        return bool(pattern.search(text))
    return f


def text_startswith(*substrings, caption: bool = False):
    def f(obj: dict[str, t.Any]):
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
    def f(obj: dict[str, t.Any]):
        return obj.get("chat", {}).get("id") in chat_ids
    return f

def chat_types(*chat_types: str):
    """
    Generates a filter that checks for matching `chat_types`.  
    
    Valid chat types are:  
    * "private"
    * "group"
    * "supergroup"
    * "channel"
    
    The filter returns `True` if obj["chat"]["type"] is in `chat_types`
    """
    def f(obj: dict[str, t.Any]):
        chat_type = obj.get("chat", {}).get("type")
        return chat_type in chat_types
    return f

def from_users(*user_ids: int):
    """
    Generates a filter that checks for matching `user_ids`.  
    
    The filter returns `True` if obj["from"]["id"] is in `user_ids`
    """
    def f(obj: dict[str, t.Any]):
        from_id = obj.get("from", {}).get("id")
        return from_id in user_ids
    return f

def callback_data(*data: str):
    """
    This filter generator is meant to use for `callback_query` updates.
    
    Generates a filter that checks for matching `data`.  
    
    The filter returns `True` if obj["data"] is in `data`
    """
    def f(obj: dict[str, t.Any]):
        cb_data = obj.get("data", "")
        return cb_data in data
    return f

def callback_data_startswith(*substrings: str):
    """
    This filter generator is meant to use for `callback_query` updates.
    
    Generates a filter that checks if `data` startswith any of the provided substrings.  
    
    The filter returns `True` if obj["data"] startswith any of the provided substrings
    """
    def f(obj: dict[str, t.Any]):
        cb_data: str = obj.get("data", "")
        return any(cb_data.startswith(s) for s in substrings)
    return f


def not_(filter: t.Callable[[dict[str, t.Any]], bool]):
    """
    shorthand for 
    ```python
    lambda obj: not filter(obj)
    ```
    """
    return lambda obj: not filter(obj)

def any_(*filters: t.Callable[[dict[str, t.Any]], bool]):
    """
    shorthand for 
    ```python
    lambda obj: any(f(obj) for f in filters)
    ```
    """
    return lambda obj: any(f(obj) for f in filters)

def all_(*filters: t.Callable[[dict[str, t.Any]], bool]):
    """
    shorthand for 
    ```python
    lambda obj: all(f(obj) for f in filters)
    ```
    """
    return lambda obj: all(f(obj) for f in filters)

def none_(*filters: t.Callable[[dict[str, t.Any]], bool]):
    """
    shorthand for 
    ```python
    lambda obj: not any(f(obj) for f in filters)
    ```
    """
    return lambda obj: not any(f(obj) for f in filters)

def xor(*filters: t.Callable[[dict[str, t.Any]], bool]):
    """
    shorthand for 
    ```python
    lambda obj: sum(bool(f(obj)) for f in filters) == 1
    ```
    """
    return lambda obj: sum(bool(f(obj)) for f in filters) == 1

is_text = keys("text")
"""`True` if "text" is in obj.keys()"""

has_caption = keys("caption")
"""`True` if "caption" is in obj.keys()"""

contains_text = keys("text", "caption")
"""`True` if either "text" or "caption" is in obj.keys()"""

is_photo = keys("photo")
"""`True` if "photo" is in obj.keys()"""

is_video = keys("video")
"""`True` if "video" is in obj.keys()"""

is_document = keys("document")
"""`True` if "document" is in obj.keys()"""

is_reply = keys("reply_to_message")
"""`True` if "reply_to_message" is in obj.keys()"""

