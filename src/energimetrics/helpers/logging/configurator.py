"""Global Loguru configuration for Energimetrics applications."""

import sys

from loguru import logger

from energimetrics.helpers.logging.config import LoggingConfig

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DDTHH:mm:ss[Z]!UTC}</green> | "
    "<level>{level:<8}</level> | "
    "<cyan>{name}</cyan> | "
    "<level>{message}</level>"
)


class LoggingConfigurator:
    """Apply a logging configuration to Loguru when explicitly requested."""

    def __init__(self, config: LoggingConfig) -> None:
        self._config = config

    def configure(self) -> None:
        """Replace existing handlers with the standard stderr sink."""
        logger.remove()
        logger.add(
            sys.stderr, level=self._config.level, format=LOG_FORMAT, colorize=True
        )
