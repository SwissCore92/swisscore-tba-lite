import typing as t
from asyncio import iscoroutinefunction
from functools import wraps

from aiohttp import ClientResponse as _ClientResponse

from ..utils import sanitize_token
from .logger import logger

def deprecated(new_func):
    def decorator(func):
        msg = f"{func.__name__} is deprecated and will be removed in the future. Use {new_func.__name__} instead!"
        
        if iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                logger.warning(msg)
                return await func(*args, **kwargs)
            
            return async_wrapper
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.warning(msg)
            return func(*args, **kwargs)
        
        return wrapper 
    
    return decorator
            

def raise_for_not_coro(func: t.Callable) -> None:
    if not iscoroutinefunction(func):
        raise TypeError(
            f"Expected couroutine but got regular function (line: {func.__code__.co_firstlineno}). "
            f"Replace `def {func.__name__}` with `async def {func.__name__}`"
        )

def raise_for_coro(func: t.Callable) -> None:
    if iscoroutinefunction(func):
        raise TypeError(
            f"Expected reqular function but got coroutine (line: {func.__code__.co_firstlineno}). "
            f"Replace `asnyc def {func.__name__}` with `def {func.__name__}`"
        )

def raise_for_non_matching_arg_count(func: t.Callable, expected_arg_count=0) -> None:
    arg_count = func.__code__.co_argcount
    if arg_count != expected_arg_count:
        raise TypeError(
            f"{func.__name__} (line: {func.__code__.co_firstlineno}) must take exactly {expected_arg_count} positional argument(s) "
            f"but gets {arg_count}."
        )

class FileProcessingError(Exception):
    """raised when file processing failed while preparing a request."""
    
class InvalidParamsError(Exception): 
    """raised when param serialization failed while preparing a request, mostly due wrong param data type."""

class MaxRetriesExeededError(Exception): 
    """raised when a request exceeded `max_retries`."""

class ResultConversionError(Exception):
    """raised on any Exception in result convertion function."""

class EventHandlerError(Exception): 
    """raised on any Exception in an event handler."""

class FilterEvaluationError(Exception): 
    """raised on any Exception while evaluating event handler filters."""

class RestartBotException(Exception):
    """raise this exception in an event handler to force the bot to restart.  
    
    **Note**: Cannot be used in startup or shutdown event handler!   
    
    Shuts down with ``exit_code`` 1
    """

class TelegramAPIError(Exception):
    """Base exception for all Telegram API errors."""
    def __init__(self, method_name, status_code, message="Unknown Error", retryable=False, retry_after=None, critical=False):
        self.method_name = method_name
        self.status_code = status_code
        self.message = message
        self.retryable = retryable
        self.retry_after = retry_after
        self.critical = critical
        super().__init__(f"'{method_name}' -> HTTP {status_code}: {message}")


class BadRequest(TelegramAPIError):
    """400 - Bad request, usually caused by invalid parameters."""
    def __init__(self, method_name, status_code=400, message="Bad Request"):
        super().__init__(method_name, status_code, message, retryable=False)


class Unauthorized(TelegramAPIError):
    """401 - Invalid bot token or unauthorized access. Critical error."""
    def __init__(self, method_name, status_code=401, message="Unauthorized"):
        super().__init__(method_name, status_code, message, retryable=False, critical=True)


class Forbidden(TelegramAPIError):
    """403 - Bot doesn't have permission for the requested action."""
    def __init__(self, method_name, status_code=403, message="Forbidden"):
        super().__init__(method_name, status_code, message, retryable=False)


class NotFound(TelegramAPIError):
    """404 - Resource not found (e.g., invalid API endpoint)."""
    def __init__(self, method_name, status_code=404, message="Not Found"):
        super().__init__(method_name, status_code, message, retryable=False)


class Conflict(TelegramAPIError):
    """409 - Conflict (e.g., webhook set but polling attempted). Critical error."""
    def __init__(self, method_name, status_code=409, message="Conflict - Webhook vs Polling Issue"):
        super().__init__(method_name, status_code, message, retryable=False, critical=True)


class PayloadTooLarge(TelegramAPIError):
    """413 - Payload (message or file) too large."""
    def __init__(self, method_name, status_code=413, message="Payload Too Large"):
        super().__init__(method_name, status_code, message, retryable=False)


class TooManyRequests(TelegramAPIError):
    """429 - Rate limit exceeded, retry after a specified time."""
    def __init__(self, method_name, status_code=429, message="Too Many Requests", retry_after=5):
        super().__init__(method_name, status_code, message, retryable=True, retry_after=retry_after)


class InternalServerError(TelegramAPIError):
    """500 - Telegram server-side issue, usually retryable."""
    def __init__(self, method_name, status_code=500, message="Internal Server Error"):
        super().__init__(method_name, status_code, message, retryable=True, retry_after=20)


class BadGateway(TelegramAPIError):
    """502 - Telegram is down or having temporary issues."""
    def __init__(self, method_name, status_code=502, message="Bad Gateway"):
        super().__init__(method_name, status_code, message, retryable=True, retry_after=20)


class GatewayTimeout(TelegramAPIError):
    """504 - Telegram's servers are taking too long to respond."""
    def __init__(self, method_name, status_code=504, message="Gateway Timeout"):
        super().__init__(504, method_name, method_name, status_code, message, retryable=True, retry_after=20)


async def raise_for_telegram_error(method_name: str, response: _ClientResponse) -> None:

    if response.status < 400:
        return
    
    if response.status < 500:
        response_json: dict[str] = await response.json()
        description = response_json.get("description", "No description available.")
    else:
        response_json = {}
        description = await response.text()

    error_map = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: NotFound,
        409: Conflict,
        413: PayloadTooLarge,
        # 429: TooManyRequests,
        500: InternalServerError,
        502: BadGateway,
        504: GatewayTimeout,
    }
    
    exc: Exception | None = None

    if response.status == 429:
        exc = TooManyRequests(method_name, response.status, description, response_json.get("retry_after", 5))
    
    if response.status == 404:
        exc = NotFound(method_name, response.status, description + f" URL: '{sanitize_token(response.url)}'")
    
    else:
        exception = error_map.get(response.status, TelegramAPIError)
        exc = exception(method_name, response.status, description)
    
    raise exc

