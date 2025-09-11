import typing as t
from asyncio import iscoroutinefunction

JsonDict = dict[str, t.Any]

def false_on_key_error(func):
    """
    This is a helper decorator that returns false if a `KeyError` is raised during filter evaluation.  
    
    Can be used for both regular and coroutine functions.
    
    Usage: 
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
