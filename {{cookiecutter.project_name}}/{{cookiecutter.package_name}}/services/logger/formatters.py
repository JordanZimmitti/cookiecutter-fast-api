from logging import Formatter
from typing import Any, Dict, Union

from {{cookiecutter.package_name}}.core.cache import get_fast_api_context
from {{cookiecutter.package_name}}.core.settings import settings


class BaseFormatter(Formatter):

    # Set of known logging attributes
    _LOGGING_ATTRIBUTES = {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
    }

    # Logger time format
    _TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def fallback_type(object_to_log: Any) -> Union[str, int, bool, float, type(None)]:
        """
        Function that gets the type of the object to log and
        casts it to a string when it is not a primitive type

        :param object_to_log: The object that will be logged
        """

        # Quote string types when not already quoted
        if isinstance(object_to_log, str):
            if '"' not in object_to_log:
                return f'"{object_to_log}"'

        # When the object to log is not a primitive cast it to a string
        if not isinstance(object_to_log, (int, bool, float, type(None))):
            return f"{str(object_to_log)}"

        # When the object to log is a primitive type
        else:
            return object_to_log

    @staticmethod
    def _get_correlation_id() -> str | None:
        """
        Function that gets the correlation-id
        from the fast-api-context

        :return: The correlation-id
        """

        # Gets the correlation-id from the fast-api-context
        fast_api_context = get_fast_api_context()
        correlation_id = fast_api_context.correlation_id_var
        return correlation_id

    @staticmethod
    def set_final_message(record):
        """
        Function that gets the raw record message and prepares
        it to be logged by the logger

        :param record: A log record
        """

        # Sets the record message
        record.message = str(record.msg)
        if record.args:
            record.message = record.message % record.args

    def get_output_items(self, record):
        """
        Function that gets the output data
        items from the record

        :param record: A log record
        """

        # Sets the basic log output data
        output = {
            "correlation_id": self._get_correlation_id(),
            "message": self.formatMessage(record),
            "level": record.levelname,
            "logger": record.name,
            "process": record.process,
            "threadname": record.threadName,
            "timestamp": "%s.%03d" % (self.formatTime(record, self._TIME_FORMAT), record.msecs),
        }

        # Sets the error log output data
        if record.exc_info:
            output["error"] = {
                "stack_trace": f'"{self.formatException(record.exc_info)}"',
            }

        # Adds the extra data when it exists
        output.update(self._get_extra_data(record))

        # Returns the log output data
        return output

    def _get_extra_data(self, record) -> Dict:
        """
        Function that parses the extra data from the record
        to be logged

        :param record: A log record
        """

        # Gets the extra data from the record
        result = {}
        for item in record.__dict__:
            if item not in self._LOGGING_ATTRIBUTES:
                value = getattr(record, item)
                result[item] = self.fallback_type(value)

        # Returns the parsed extra data
        return result


class LineFormatter(BaseFormatter):
    def format(self, record):
        """
        Function that formats the
        log data to log

        :param record: A log record
        """

        # Sets the final message from the record
        self.set_final_message(record)

        # Gets the items from the output
        output = self.get_output_items(record)
        correlation_id = output.pop("correlation_id")
        level = output.pop("level")
        logger = output.pop("logger")
        message = output.pop("message")
        process = output.pop("process")
        threadname = output.pop("threadname")
        timestamp = output.pop("timestamp")

        # Gets the error when it exists
        if "error" in output:
            error = output.pop("error")
        else:
            error = None

        # Creates the logger prefix template
        prefix = (
            f'host="{settings.HOSTNAME}" -- '
            f"process={process} -- "
            f'threadname="{threadname}" -- '
            f'timestamp="{timestamp}" -- '
            f'correlation_id="{correlation_id}" -- '
            f'level="{level}" logger="{logger}" message="{message}"'
        )

        # Gets extra components to add to the logger template
        components = [prefix]
        for key, value in output.items():
            component = f"{key}={self.fallback_type(value)}"
            components.append(component)
        if error:
            stack_trace = error["stack_trace"]
            components.append(f"error={stack_trace}")

        # Adds the extra components to the line log
        line = " ".join(components)
        return line
