import sys
import logging
from pathlib import Path
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
LOG_LEVEL = logging.INFO
LOG_FILE = LOGS_DIR / f"agent_{datetime.now().strftime('%Y%m%d')}.log"

# Create a logger
logger = logging.getLogger("agent_logger")
logger.setLevel(LOG_LEVEL)

# Clear existing handlers if any
if logger.hasHandlers():
    logger.handlers.clear()

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")

# Set levels for handlers
console_handler.setLevel(LOG_LEVEL)
file_handler.setLevel(LOG_LEVEL)

# Create formatter
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Add formatter to handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Export only the logger
__all__ = ["logger"]