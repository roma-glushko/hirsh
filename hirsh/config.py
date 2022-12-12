import logging
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseSettings, Field

logger = logging.getLogger(__name__)


class TelegramConfig(BaseSettings):
    bot_token: str
    channel_ids: list[int]


class DatabaseConfig(BaseSettings):
    uri: str  # TODO: Create SQLiteDns type (see pydantic.PostgresDsn)


class LoggingConfig(BaseSettings):
    level: str = "INFO"


class MonitoringConfig(BaseSettings):
    check_every_secs: int = 60


class Config(BaseSettings):
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    telegram: Optional[TelegramConfig] = Field(None)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)


class ConfigReadFailed(RuntimeError):
    """
    Occurs when it's impossible to read the given YAML config file
    """


def load_from_yaml(config_path: Path) -> Config:
    config_path = config_path.expanduser()

    logger.debug(f"Reading '{config_path}' config file")

    if not config_path.is_file():
        raise ConfigReadFailed(f"'{config_path}' config file doesn't exist or not readable")

    with open(config_path, "r") as file:
        try:
            raw_config: dict[str, Any] = yaml.safe_load(file)

            return Config.parse_obj(raw_config)
        except yaml.YAMLError as e:
            raise ConfigReadFailed(f"Failed to read '{config_path}' config file") from e
