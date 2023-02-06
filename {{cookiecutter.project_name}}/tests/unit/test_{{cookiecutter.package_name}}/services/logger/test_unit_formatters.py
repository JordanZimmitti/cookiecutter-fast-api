from logging import LogRecord
from unittest.mock import MagicMock

from {{cookiecutter.package_name}}.core.cache import FastApiContext
from {{cookiecutter.package_name}}.services.logger import formatters
from {{cookiecutter.package_name}}.services.logger.formatters import BaseFormatter, LineFormatter


def test_fallback_type_int():
    """
    Tests the fallback_type function when the object-to-log is an int.
    The fallback_type function should return the int without changing
    its type
    """

    # Checks whether the int was retrieved without its type changing
    log_object = BaseFormatter.fallback_type(0)
    assert log_object == 0


def test_fallback_type_object():
    """
    Tests the fallback_type function when the object-to-log is not a primitive object or None.
    The fallback_type function should return the object as a string
    """

    # Creates an example message
    message = {"message": "test-message"}

    # Checks whether the no-primitive dict type is represented as a string
    log_object = BaseFormatter.fallback_type(message)
    assert log_object == "{'message': 'test-message'}"


def test_fallback_type_quote_string():
    """
    Tests the fallback_type function when the object-to-log is an unquoted string.
    The fallback_type function should return a quoted string
    """

    # Checks whether the given unquoted string gets quoted
    log_object = BaseFormatter.fallback_type("test-message")
    assert log_object == '"test-message"'


def test_format_with_error():
    """
    Tests the format function when an error is present. The format function should
    format the log-record data into a line-log containing the error data without
    any errors
    """

    # Mocks log output data
    output_mock = {
        "correlation_id": "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2",
        "message": "hello-world",
        "level": "INFO",
        "logger": "test.logger.formatters",
        "process": 1000,
        "threadname": "MainThread",
        "timestamp": "2001-01-01.100",
        "extra_item": "extra-one",
        "error": {"stack_trace": '"FakeError: testing a fake error"'},
    }

    # Mocks the line-formatter class
    line_formatter_mock = MagicMock(spec=LineFormatter)
    line_formatter_mock.fallback_type = lambda a: a
    line_formatter_mock.get_output_items = lambda a: output_mock

    # Mocks the log-record class
    log_record_mock = MagicMock(spec=LogRecord)

    # Checks whether the log-line was retrieved correctly
    # noinspection StrFormat
    line_log = LineFormatter.format(self=line_formatter_mock, record=log_record_mock)
    assert line_log.partition("-- ")[2] == (
        "process=1000 "
        '-- threadname="MainThread" '
        '-- timestamp="2001-01-01.100" '
        '-- correlation_id="a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2" '
        '-- level="INFO" '
        'logger="test.logger.formatters" '
        'message="hello-world" '
        "extra_item=extra-one "
        'error="FakeError: testing a fake error"'
    )


def test_format_without_error():
    """
    Tests the format function when an error is not present. The format function should
    format the log-record data into a line-log without any errors
    """

    # Mocks log output data
    output_mock = {
        "correlation_id": "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2",
        "message": "hello-world",
        "level": "INFO",
        "logger": "test.logger.formatters",
        "process": 1000,
        "threadname": "MainThread",
        "timestamp": "2001-01-01.100",
        "extra_item": "extra-one",
    }

    # Mocks the line-formatter class
    line_formatter_mock = MagicMock(spec=LineFormatter)
    line_formatter_mock.fallback_type = lambda a: a
    line_formatter_mock.get_output_items = lambda a: output_mock

    # Mocks the log-record class
    log_record_mock = MagicMock(spec=LogRecord)

    # Checks whether the log-line was retrieved correctly
    # noinspection StrFormat
    line_log = LineFormatter.format(self=line_formatter_mock, record=log_record_mock)
    assert line_log.partition("-- ")[2] == (
        "process=1000 "
        '-- threadname="MainThread" '
        '-- timestamp="2001-01-01.100" '
        '-- correlation_id="a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2" '
        '-- level="INFO" '
        'logger="test.logger.formatters" '
        'message="hello-world" '
        "extra_item=extra-one"
    )


def test_get_correlation_id(mocker):
    """
    Function that tests the _get_correlation_id function for completion. The _get_correlation_id
    function should return the correlation id without any error

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the fast-api-context class
    fast_api_context_mock = MagicMock(spec_set=FastApiContext)
    fast_api_context_mock.correlation_id_var = "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2"

    # Overrides the get_fast_api_context function
    mocker.patch.object(formatters, "get_fast_api_context", return_value=fast_api_context_mock)

    # Checks whether the correlation-id was retrieved correctly
    correlation_id = BaseFormatter._get_correlation_id()
    assert correlation_id == "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2"


def test_get_extra_data():
    """
    Tests the _get_extra_data function for completion. The _get_extra_data function
    should return a dictionary containing keys that are not part of the known
    logging attributes
    """

    # Mocks the base-formatter class
    base_formatter_mock = MagicMock(spec=BaseFormatter)
    base_formatter_mock._LOGGING_ATTRIBUTES = {"test_attribute_one", "test_attribute_two"}
    base_formatter_mock.fallback_type = lambda a: a

    # Mocks the log-record class
    log_record_mock = MagicMock(spec=LogRecord)
    log_record_mock.test_attribute_one = "test-attribute-one"
    log_record_mock.test_attribute_two = "test-attribute-two"
    log_record_mock.extra_one = "extra-one"
    log_record_mock.extra_two = "extra-two"

    # Checks whether the extra data was retrieved correctly
    extra_data = BaseFormatter._get_extra_data(self=base_formatter_mock, record=log_record_mock)
    assert extra_data.get("test_attribute_one") is None
    assert extra_data.get("test_attribute_two") is None
    assert extra_data.get("extra_one") == "extra-one"
    assert extra_data.get("extra_two") == "extra-two"


def test_get_output_items():
    """
    Tests the get_output_items function for completion. The get_output_items function should
    return an output dictionary created from a log-record
    """

    # Mocks the base-formatter class
    base_formatter_mock = MagicMock(spec=BaseFormatter)
    base_formatter_mock._TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    base_formatter_mock.formatException = lambda a: a
    base_formatter_mock.formatMessage = lambda a: "hello-world"
    base_formatter_mock.formatTime = lambda a, b: "2001-01-01"
    base_formatter_mock._get_correlation_id = lambda: "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2"
    base_formatter_mock._get_extra_data = lambda a: {}

    # Mocks the log-record class
    log_record_mock = MagicMock(spec=LogRecord)
    log_record_mock.exc_info = "FakeError: testing a fake error"
    log_record_mock.levelname = "INFO"
    log_record_mock.msecs = 100.01
    log_record_mock.name = "test.logger.formatters"
    log_record_mock.process = 1000
    log_record_mock.threadName = "MainThread"

    # Checks whether the output was retrieved correctly
    output = BaseFormatter.get_output_items(self=base_formatter_mock, record=log_record_mock)
    assert output == {
        "correlation_id": "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2",
        "message": "hello-world",
        "level": "INFO",
        "logger": "test.logger.formatters",
        "process": 1000,
        "threadname": "MainThread",
        "timestamp": "2001-01-01.100",
        "error": {"stack_trace": '"FakeError: testing a fake error"'},
    }


def test_set_final_message():
    """
    Tests the set_final_message function for completion. The set_final_message function
    should prepare the message to be logged by the logger
    """

    # Mocks the log-record class
    log_record_mock = MagicMock(spec=LogRecord)
    log_record_mock.msg = "hello-world %d"
    log_record_mock.args = (1,)

    # Invokes the set_final_message function
    BaseFormatter.set_final_message(log_record_mock)

    # Checks whether the message was prepared correctly
    assert log_record_mock.message == "hello-world 1"
