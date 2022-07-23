from typing import Tuple
from uuid import uuid4

from fastapi import Request, Response

from {{cookiecutter.package_name}}.core.cache import FastApiContext


def get_response_size(response: Response) -> int:
    """
    Dependency function that gets the
    size of the response in bytes

    :param response: The response to the client

    :return: The response size
    """

    # Attempts to get the response size
    try:

        # Gets the response size when it exists
        if "content-length" in response.headers:
            response_size = int(response.headers.get("content-length"))  # bytes

        # Sets the response size as zero
        else:
            response_size = 0

    # When the response size exists but can't be parsed, set the response size as zero
    except ValueError:
        response_size = 0

    # Returns the response size
    return response_size


def get_request_metadata(request: Request) -> Tuple[str, str, str]:
    """
    Dependency function that gets the request
    metadata that is used for logging

    :param request: The request sent by the client

    :return: The request metadata (method, url, user_agent)
    """

    # Gets the request metadata
    method = request.method
    url = str(request.url)
    user_agent = request.headers.get("user-agent")

    # Returns the request metadata
    return method, url, user_agent


def set_correlation_id(request: Request, fast_api_context: FastApiContext):
    """
    Dependency function that sets the correlation-id. Once the correlation-id
    is set it can now be written to all logs from the start of the request to
    when the response is sent back to the client

    :param request: The request sent by the client
    :param fast_api_context: The FastAPI thread-safe context-manager
    """

    # Gets the correlation-id
    if "x-correlation-id" in request.headers:
        correlation_id = request.headers["x-correlation-id"]
    else:
        correlation_id = str(uuid4())

    # Sets the correlation-id
    fast_api_context.correlation_id_var = correlation_id
