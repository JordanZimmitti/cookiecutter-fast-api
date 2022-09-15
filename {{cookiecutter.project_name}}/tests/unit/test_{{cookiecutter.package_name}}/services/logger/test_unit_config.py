from os import removedirs
from os.path import exists

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.services.logger import config

# noinspection PyProtectedMember
from {{cookiecutter.package_name}}.services.logger.config import _get_logger_config, start_logger
from {{cookiecutter.package_name}}.utils.modules.path_extensions import get_parent_path_by_file


def test_start_logger(mocker):
    """
    Tests the start_logger for completion. The start_logger function
    should start the custom logger without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks and overrides the _get_logger_config function
    log_config_mock = {"version": 1, "loggers": {"": {}}}
    mocker.patch.object(config, "_get_logger_config", return_value=log_config_mock)

    # Invokes the start_logger function
    start_logger("INFO")


def test_get_logger_config():
    """
    Tests the _get_logger_config function for completion. The _get_logger_config function
    should get the logger configuration dictionary without any errors
    """

    # Removes the log directory
    project_path = f"{get_parent_path_by_file('pyproject.toml')}"
    log_directory = f"{project_path}/{settings.LOG_FILE_DIRECTORY}/"
    if exists(log_directory):
        removedirs(log_directory)

    # Gets the logger config
    _get_logger_config()
