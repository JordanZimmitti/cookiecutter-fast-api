from contextvars import ContextVar


class FastApiContext:
    def __init__(self):
        """
        Class that is used to create context variables for fast-api requests. Context variables
        are special variables that are thread safe. Because of this, we can utilize context
        variables that can store values for the length of a request without the worry of the
        value being overwritten by another request
        """

        # Creates the context variables
        self._correlation_id_var = ContextVar("correlation_id")
        self._request_url_var = ContextVar("request_url_var")

    @property
    def correlation_id_var(self) -> str | None:
        """
        Function that gets the thread safe
        correlation-id value

        :return: The correlation-id value
        """
        correlation_id = self._correlation_id_var.get(None)
        return correlation_id

    @property
    def request_url_var(self) -> str | None:
        """
        Function that gets the thread safe
        request URL value

        :return: The request URL value
        """
        request_url = self._request_url_var.get(None)
        return request_url

    @correlation_id_var.setter
    def correlation_id_var(self, correlation_id: str):
        """
        Function that sets the thread safe
        correlation-id value

        :param correlation_id: The id used to correlate all the logs together for a single request
        """
        self._correlation_id_var.set(correlation_id)

    @request_url_var.setter
    def request_url_var(self, request_url: str):
        """
        Function that sets the thread safe
        request URL value

        :param request_url: A request URL
        """
        self._request_url_var.set(request_url)

    def reset(self):
        """
        Function that resets the context variables
        to their initial state
        """
        self._correlation_id_var.set(None)
        self._request_url_var.set(None)


# Creates the fast-api context instance
_fast_api_context = FastApiContext()


def get_fast_api_context() -> FastApiContext:
    """
    Function that gets the fast-api-context
    instance

    :return: The fast-api-context instance
    """
    return _fast_api_context
