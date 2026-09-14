"""Global Loguru configuration for Energimetrics applications."""

import sys

from loguru import logger

from energimetrics.helpers.logging.config import LoggingConfig

LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name} | {message}"


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
