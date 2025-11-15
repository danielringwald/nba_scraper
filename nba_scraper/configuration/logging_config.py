# nba_scraper/configuration/logging_config.py
import logging
import logging.handlers
import os

# Logs folder relative to project root
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "nba_scraper.log")


def init_logging():
    """
    Initialize logging for the project:
    - Rotating file handler (DEBUG+)
    - Console handler (INFO+)
    - Force=True ensures configuration applies even if logging was partially initialized
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.handlers.RotatingFileHandler(
                LOG_FILE_PATH, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
            ),
            logging.StreamHandler()
        ],
        force=True,  # ensures config is applied even if loggers already exist
    )
