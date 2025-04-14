import sys
import logging
from pathlib import Path

LOG_FILE = Path("swissore_tba_lite.log")

try:
    if "--no-colors" in sys.argv:
        raise ModuleNotFoundError
    
    import colorama
    from colorama import Fore, Style, Back

    colorama.init(autoreset=True)

    class ColoredFormatter(logging.Formatter):
        COLORS = {
            logging.DEBUG: Back.BLACK + Fore.LIGHTBLACK_EX,
            logging.INFO: Back.BLACK + Fore.WHITE,
            logging.WARNING: Back.BLACK + Fore.YELLOW, 
            logging.ERROR: Back.BLACK + Fore.RED,
            logging.CRITICAL: Back.RED + Fore.WHITE,
        }

        def format(self, record):
            color = self.COLORS.get(record.levelno, Fore.WHITE)
            log_message = super().format(record)
            return color + log_message + Style.RESET_ALL
        
except ModuleNotFoundError:
    class ColoredFormatter(logging.Formatter): ...

class Logger(logging.Logger):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.INFO
    CRITICAL = logging.CRITICAL
    
    def __init__(self, name: str, level=logging.DEBUG):
        super().__init__(name, level)
        
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(Logger.DEBUG)
        self.console_handler.setFormatter(
            ColoredFormatter("%(levelname)s: %(message)s")
        )
        self.addHandler(self.console_handler)

        self.file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        self.file_handler.setLevel(Logger.DEBUG)
        self.file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.addHandler(self.file_handler)
    
    def flush_file(self):
        self.debug(f"Flushing log file")
        self.file_handler.flush()

    def set_level(self, level: int):
        """set logger level (only affects console handler)."""
        self.console_handler.setLevel(level)

logging.setLoggerClass(Logger)

logger = Logger("swisscore_tba_lite", Logger.DEBUG)
