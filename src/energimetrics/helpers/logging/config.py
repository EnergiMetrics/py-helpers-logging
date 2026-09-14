"""Application-composable logging configuration."""

from typing import Literal

from pydantic import BaseModel

LogLevel = Literal["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]


class LoggingConfig(BaseModel):
    """The minimum level emitted by the application logger."""

    level: LogLevel = "INFO"
