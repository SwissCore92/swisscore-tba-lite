import typing as t

from .helpers import JsonDict


def if_not(filter: t.Callable[[JsonDict], bool]):
    """
    shorthand for 
    ```python
    lambda obj: not filter(obj)
    ```
    """
    return lambda obj: not filter(obj)

def if_any(*filters: t.Callable[[JsonDict], bool]):
    """
    shorthand for 
    ```python
    lambda obj: any(f(obj) for f in filters)
    ```
    """
    return lambda obj: any(f(obj) for f in filters)

def if_all(*filters: t.Callable[[JsonDict], bool]):
    """
    shorthand for 
    ```python
    lambda obj: all(f(obj) for f in filters)
    ```
    """
    return lambda obj: all(f(obj) for f in filters)

def if_none(*filters: t.Callable[[JsonDict], bool]):
    """
    shorthand for 
    ```python
    lambda obj: not any(f(obj) for f in filters)
    ```
    """
    return lambda obj: not any(f(obj) for f in filters)

def if_xor(*filters: t.Callable[[JsonDict], bool]):
    """
    shorthand for 
    ```python
    lambda obj: sum(bool(f(obj)) for f in filters) == 1
    ```
    """
    return lambda obj: sum(bool(f(obj)) for f in filters) == 1
