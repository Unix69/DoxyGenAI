import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv




load_dotenv()

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "doxygen_ai_crew.log")


os.makedirs(LOG_DIR, exist_ok=True)

# Colori ANSI per console
COLORS = {
    "DEBUG": "\033[94m",    # blu chiaro
    "INFO": "\033[92m",     # verde
    "WARNING": "\033[93m",  # giallo
    "ERROR": "\033[91m",    # rosso
    "CRITICAL": "\033[41m", # sfondo rosso
    "RESET": "\033[0m"      # reset
}

# Formatter base (file)
file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Formatter colorato per console
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, COLORS["RESET"])
        # Coloriamo solo levelname
        record.levelname = f"{color}{record.levelname}{COLORS['RESET']}"
        return super().format(record)

console_formatter = ColoredFormatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Logger principale
logger = logging.getLogger("DoxygenAICrew")
logger.setLevel(logging.DEBUG)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # INFO+ sulla console
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File Handler
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)



