# modules/logger.py
import logging
from pathlib import Path

def setup_logger():
    logger = logging.getLogger("CCTV_Detection")
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create a file handler
    log_file = log_dir / "app.log"
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

logger = setup_logger()
