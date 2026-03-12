import logging
from logging.handlers import RotatingFileHandler
from .settings import settings

def setup_logger(name: str = "foodbot"):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), "INFO"))

    # Rotating File Handler
    handler = RotatingFileHandler(
        "logs/foodbot.log",
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger

logger = setup_logger()