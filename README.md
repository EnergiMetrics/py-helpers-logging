# Energimetrics Logging Helper

A small class-based Loguru configuration helper for Energimetrics Python applications.

Install with uv:

```sh
uv add "energimetrics.helpers.logging @ git+https://github.com/EnergiMetrics/py-helpers-logging.git"
```

Compose `LoggingConfig` into your application's Pydantic model:

```python
from pydantic import BaseModel

from energimetrics.helpers.logging import LoggingConfig


class Config(BaseModel):
    logging: LoggingConfig
```

For example, your configuration can contain:

```yaml
logging:
  level: INFO
```

Configure Loguru after loading application configuration:

```python
from loguru import logger

from energimetrics.helpers.logging import LoggingConfigurator

config = ConfigLoader("config.yaml", Config).load()

LoggingConfigurator(config.logging).configure()

logger.info("Starting application")
```

`LoggingConfigurator` configures the global Loguru logger. Applications and Energimetrics helpers, including config and MQTT, continue to log with `from loguru import logger`; their messages share the configured level and format after `configure()` runs. Config-loader messages emitted before then may use Loguru's initial configuration. This is expected in 0.1.0.
