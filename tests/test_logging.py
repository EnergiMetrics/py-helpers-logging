"""Public configuration and global Loguru behavior."""

import re
import sys
from collections.abc import Iterator
from datetime import UTC, datetime

import pytest
from loguru import logger
from pydantic import BaseModel, ValidationError

from energimetrics.helpers.logging import LoggingConfig, LoggingConfigurator


@pytest.fixture
def restore_logger() -> Iterator[None]:
    """Isolate tests that modify Loguru's global handlers."""
    stderr = sys.__stderr__
    assert stderr is not None
    logger.remove()
    logger.add(stderr)
    yield
    logger.remove()
    logger.add(stderr)


def test_default_level() -> None:
    assert LoggingConfig().level == "INFO"


@pytest.mark.parametrize(
    "level",
    ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"],
)
def test_valid_levels(level: str) -> None:
    assert LoggingConfig.model_validate({"level": level}).level == level


def test_invalid_level() -> None:
    with pytest.raises(ValidationError):
        LoggingConfig.model_validate({"level": "VERBOSE"})


def test_composes_in_application_model() -> None:
    class AppConfig(BaseModel):
        logging: LoggingConfig

    assert (
        AppConfig.model_validate({"logging": {"level": "DEBUG"}}).logging.level
        == "DEBUG"
    )


def test_construction_has_no_global_effect(restore_logger: None) -> None:
    messages: list[str] = []
    logger.remove()
    logger.add(lambda message: messages.append(str(message)), format="{message}")

    LoggingConfigurator(LoggingConfig())
    logger.info("still original")

    assert messages == ["still original\n"]


def test_configure_replaces_handlers_and_writes_standard_stderr(
    restore_logger: None,
    capsys: pytest.CaptureFixture[str],
) -> None:
    old_messages: list[str] = []
    logger.add(lambda message: old_messages.append(str(message)))

    before = datetime.now(UTC)
    result = LoggingConfigurator(LoggingConfig()).configure()
    logger.info("Starting application")
    after = datetime.now(UTC)

    captured = capsys.readouterr()
    assert result is None
    assert old_messages == []
    assert captured.out == ""
    match = re.fullmatch(
        r"\x1b\[32m(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\x1b\[0m \| "
        r"\x1b\[1mINFO    \x1b\[0m \| "
        r"\x1b\[36mtest_logging\x1b\[0m \| "
        r"\x1b\[1mStarting application\x1b\[0m\n",
        captured.err,
    )
    assert match is not None
    timestamp = datetime.fromisoformat(match.group("timestamp"))
    assert before.replace(microsecond=0) <= timestamp <= after.replace(microsecond=0)


def test_configured_level_filters_messages(
    restore_logger: None, capsys: pytest.CaptureFixture[str]
) -> None:
    LoggingConfigurator(LoggingConfig(level="WARNING")).configure()
    logger.info("below")
    logger.warning("at level")
    logger.error("above")

    output = capsys.readouterr().err
    assert "below" not in output
    assert "WARNING" in output and "at level" in output
    assert "ERROR" in output and "above" in output


def test_reconfiguration_does_not_duplicate_output(
    restore_logger: None,
    capsys: pytest.CaptureFixture[str],
) -> None:
    configurator = LoggingConfigurator(LoggingConfig())
    configurator.configure()
    configurator.configure()
    logger.info("once")

    assert capsys.readouterr().err.count("once") == 1
