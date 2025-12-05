import sys
from typing import Optional

from loguru import logger

from .config import get_settings


def configure_logging(level: Optional[str] = None) -> None:
    settings = get_settings()
    log_level = level or settings.LOG_LEVEL

    logger.remove()
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {name}:{line} | {message}",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )


def get_logger():
    return logger
