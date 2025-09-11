
TERMITATED_BY_USER = 0
"""Bot was shut down manually by the user."""

RESTART = 1
"""Bot was forced to restart by `RestartBotException`"""

UNEXPECTED_ERROR = 2
"""Bot was shut down by an unexpected error."""

CRITICAL_TELEGRAM_ERROR = 3
"""Bot was shut down by a critical Telegram API error while getting updates. (403: Forbidden or 409: Conflict)"""

UNEXPECTED_TELEGRAM_ERROR = 4
"""Bot was shut down by a unexpected Telegram API error while getting updates. (Should not happen in theory)"""


