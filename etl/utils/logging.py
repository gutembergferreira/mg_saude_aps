import sys
from loguru import logger


def configure_etl_logging(level: str = "INFO") -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )


def get_logger():
    return logger
