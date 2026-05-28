from logging import Filter

from {{cookiecutter.package_name}}.core.cache.fast_api_context import get_fast_api_context


class RequestFilter(Filter):
    """
    Filter class that stops certain
    requests from being logged
    """

    def filter(self, record) -> bool:

        # Gets the request URL when it exists
        fast_api_context = get_fast_api_context()
        request_url = fast_api_context.request_url_var

        # Checks whether a request URL should not be logged
        if request_url and "/health/check" in request_url:
            return False

        # Returns that the request should not be filtered
        return True
