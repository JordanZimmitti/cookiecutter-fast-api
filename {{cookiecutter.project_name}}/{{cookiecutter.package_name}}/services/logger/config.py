from logging import getLogger
from logging.config import dictConfig
from os import makedirs
from os.path import exists
from typing import Any, Dict

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.utils.path_utils import get_parent_path_by_file

from .filters import RequestFilter


def get_api_logger(name: str):
    """
    Function that gets an API logger. Centralized filters
    are added to the logger in this function

    :param name: The name of the logger

    :return: A logger instance
    """

    # Gets the logger
    logger = getLogger(name)
    logger.addFilter(RequestFilter())

    # Returns the API logger
    return logger


def start_logger(log_level: str):
    """
    Function that starts
    the logger

    :param log_level: The amount of data that should be outputted by the logs
    """

    # Sets the logger environment
    logger = _get_logger_config()
    logger["loggers"][""]["level"] = log_level
    dictConfig(logger)


def _get_logger_config() -> Dict[str, Any]:
    """
    Function that configures and gets the custom API logger

    :return: The custom API logger
    """

    # Creates the log file directory when it does not exist
    project_path = f"{get_parent_path_by_file('pyproject.toml')}"
    log_directory = f"{project_path}/{settings.LOG_FILE_DIRECTORY}/"
    if not exists(log_directory):
        makedirs(log_directory, exist_ok=True)

    # Returns the logger configuration dict
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "line": {"class": "{{cookiecutter.package_name}}.services.logger.formatters.LineFormatter"},
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "formatter": "line",
                "stream": "ext://sys.stdout",
            },
            "logging": {
                "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",
                "formatter": "line",
                "filename": f"{log_directory}/{settings.HOSTNAME}.log",
                "mode": "a",
                "maxBytes": settings.LOG_FILE_MAX_BYTES,
                "backupCount": settings.LOG_FILE_BACKUP_COUNT,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "": {"handlers": ["stdout", "logging"], "level": "DEBUG", "propagate": True},
            "aiosqlite": {"level": "WARNING"},
            "google": {"level": "WARNING"},
            "httpcore": {"level": "WARNING"},
            "httpx": {"level": "WARNING"},
            "multipart": {"level": "WARNING"},
            "python_multipart.multipart": {"level": "WARNING"},
        },
    }
