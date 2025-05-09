# --- app/logger.py ---
# Sets up and returns a logger for the app

import logging

def setup_logger(name="pdf_summarizer"):
    """
    Configures a logger with stream output and info level.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

