import itertools
import json
import logging
import logging.config
import os
from typing import Any, Dict, List, Literal, Optional

from .settings import HashableSettings

SILENT_HANDLERS = [
    "transitions.core",
    "botocore",
]


LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "trace": 5,
}

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "coloredlogs.ColoredFormatter",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "fmt": "%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(filename)-8s:%(funcName)s:%(lineno)-8d %(message)s",  # noqa: E501
        },
    },
    "handlers": {
        "default": {"formatter": "default", "class": "logging.StreamHandler", "stream": "ext://sys.stderr"},
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO"},
    },
}


class LogSettings(HashableSettings):
    __slots__ = ("_logging_config",)
    level: Literal["critical", "error", "warning", "info", "debug", "trace"] = "info"
    config: Optional[str] = None

    class Config:
        env_prefix = "log_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __setattr__(self, attr, value):
        if attr in self.__slots__:
            object.__setattr__(self, attr, value)
        else:
            super().__setattr__(attr, value)

    @property
    def logging_config(self) -> Dict[str, Any]:
        if getattr(self, "_logging_config", None) is None:
            self._logging_config = LOGGING_CONFIG
            if self.config is not None and os.path.exists(self.config):  # pragma: no cover
                with open(self.config) as config_file:
                    self._logging_config = json.load(config_file)
        return self._logging_config

    def apply(self, silent_handlers: List[str] = []):
        logging.config.dictConfig(self.logging_config)
        level = LOG_LEVELS[self.level]
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        for handler in root_logger.handlers:
            handler.setLevel(level)
        for name in itertools.chain(SILENT_HANDLERS, silent_handlers):
            logging.getLogger(name).disabled = True
            logging.getLogger(name).propagate = False
