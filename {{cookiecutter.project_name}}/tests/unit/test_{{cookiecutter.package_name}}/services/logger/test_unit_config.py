from unittest.mock import MagicMock

from {{cookiecutter.package_name}}.core.settings import Settings
from {{cookiecutter.package_name}}.services.logger import config

# noinspection PyProtectedMember
from {{cookiecutter.package_name}}.services.logger.config import _get_logger_config, start_logger


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
    settings_mock.LOG_FILE_MAX_BYTES =1000
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
