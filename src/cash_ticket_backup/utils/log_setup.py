import logging
import os

import click
import yaml

DEFAULT_CONFIGURATION = """
version: 1
disable_existing_loggers: false
formatters:
  verbose:
    "class" : coloredlogs.ColoredFormatter
    datefmt: "%H:%M:%S"
    format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
  simple:
    format: "%(message)s"
  server:
    (): coloredlogs.ColoredFormatter
    datefmt: "%Y-%m-%dT%H:%M:%S%z"
    format: "%(asctime)s %(message)s"
handlers:
  console:
    level: DEBUG
    class: logging.StreamHandler
    formatter: verbose
  httplog:
    level: INFO
    class: logging.StreamHandler
    formatter: server
loggers:
  server:
    handlers: [ httplog ]
    level: INFO
    propagate: no
root:
  handlers: [ console ]
  level: WARNING
"""


def setup_logging(default_path='log_config.yaml', env_key='LOG_CONFIG'):
    path = os.getenv(env_key, default_path)
    configured = False
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                configured = True
            except Exception as error:
                click.secho('>>> ', fg='red', bold=True, nl=False)
                click.secho(
                    f'Error in Logging Configuration ({error}). Using default configuration.',
                    bold=True,
                )
    if not configured:
        logging.config.dictConfig(yaml.safe_load(DEFAULT_CONFIGURATION))
