from logging import Logger
from unittest.mock import MagicMock

from example_api.core.settings import Settings
from example_api.services.logger import config

# noinspection PyProtectedMember
from {{cookiecutter.package_name}}.services.logger.config import _get_logger_config, get_api_logger, start_logger
from {{cookiecutter.package_name}}.services.logger.filters import HealthCheckFilter


def test_get_api_logger(mocker):
    """
    Tests the get_api_logger function for completion. The get_api_logger
    function should return a logger instance without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the logger class
    logger_mock = MagicMock(spec_set=Logger)

    # Mock and overrides the getLogger function
    get_logger_mock = MagicMock()
    get_logger_mock.return_value = logger_mock
    mocker.patch.object(config, "getLogger", get_logger_mock)

    # Mock and overrides the health-check-filter class
    health_check_filter_mock = MagicMock(spec_set=HealthCheckFilter)
    health_check_filter_mock.return_value = health_check_filter_mock
    mocker.patch.object(config, "HealthCheckFilter", health_check_filter_mock)

    # Invokes the get_api_logger function
    logger = get_api_logger("logger-name")

    # Checks whether the logger was retrieved correctly
    assert logger == logger_mock
    assert get_logger_mock.called
    assert get_logger_mock.call_args.args[0] == "logger-name"
    assert logger_mock.addFilter.call_count == 1
    assert logger_mock.addFilter.call_args.args[0] == health_check_filter_mock


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


def test_get_logger_config(mocker):
    """
    Tests the _get_logger_config function for completion. The _get_logger_config function
    should get the logger configuration dictionary without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.HOSTNAME = "hostname"
    settings_mock.LOG_FILE_DIRECTORY = "log-file-directory"
    settings_mock.LOG_FILE_MAX_BYTES = 1000
    settings_mock.LOG_FILE_BACKUP_COUNT = 1
    mocker.patch.object(config, "settings", settings_mock)

    # Mock and overrides the get_parent_path_by_file function
    get_parent_path_by_file_mock = MagicMock()
    get_parent_path_by_file_mock.return_value = "parent-path"
    mocker.patch.object(config, "get_parent_path_by_file", get_parent_path_by_file_mock)

    # Mock and overrides the exists function
    exists_mock = MagicMock()
    exists_mock.return_value = False
    mocker.patch.object(config, "exists", exists_mock)

    # Mock and overrides the makedirs function
    makedirs_mock = MagicMock()
    mocker.patch.object(config, "makedirs", makedirs_mock)

    # Gets the logger config
    _get_logger_config()

    # Checks whether the functions were invoked correctly
    assert get_parent_path_by_file_mock.called
    assert get_parent_path_by_file_mock.call_args.args[0] == "pyproject.toml"
    assert exists_mock.called
    assert exists_mock.call_args.args[0] == "parent-path/log-file-directory/"
    assert makedirs_mock.called
    assert makedirs_mock.call_args.args[0] == "parent-path/log-file-directory/"
