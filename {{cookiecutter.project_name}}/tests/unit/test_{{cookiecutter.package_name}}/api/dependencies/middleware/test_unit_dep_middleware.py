from unittest.mock import MagicMock
from uuid import UUID

from fastapi import Request, Response

from {{cookiecutter.package_name}}.api.dependencies.middleware import (
    get_request_metadata,
    get_response_size,
    set_correlation_id,
)
from {{cookiecutter.package_name}}.core.cache.fast_api_context import FastApiContext


def test_get_response_size_bad_value():
    """
    Tests the get_response_size function when a response size value cannot be cast as an integer.
    The get_response_size function should return a response size of zero
    """

    # Mocks the response class
    response_mock = MagicMock(spec=Response)
    response_mock.headers = {"content-length": "1000 bytes"}

    # Checks that a response size of zero is retrieved correctly
    response_size = get_response_size(response_mock)
    assert response_size == 0


def test_get_response_size_exists():
    """
    Tests the get_response_size function when a response size exists. The get_response_size
    function should return a non-zero response size
    """

    # Mocks the response class
    response_mock = MagicMock(spec=Response)
    response_mock.headers = {"content-length": 1000}

    # Checks that the correct non-zero response size is retrieved correctly
    response_size = get_response_size(response_mock)
    assert response_size == 1000


def test_get_response_size_not_exists():
    """
    Tests the get_response_size function when a response size does not exist. The get_response_size
    function should return a response size of zero
    """

    # Mocks the response class
    response_mock = MagicMock(spec=Response)

    # Checks that a response size of zero is retrieved correctly
    response_size = get_response_size(response_mock)
    assert response_size == 0


def test_get_request_metadata():
    """
    Tests the get_request_metadata function for completion. The get_request_metadata function
    should return the method, url, and user_agent without any errors
    """

    # Mocks the request class
    request_mock = MagicMock(spec=Request)
    request_mock.method = "GET"
    request_mock.url = "https://test-url"
    request_mock.headers = {"user-agent": "test-agent"}

    # Gets the request metadata
    method, url, user_agent = get_request_metadata(request_mock)

    # Checks whether the request metadata was retrieved correctly
    assert method == "GET"
    assert url == "https://test-url"
    assert user_agent == "test-agent"


def test_set_correlation_id_new():
    """
    Tests the set_correlation_id function when a new correlation id should be created.
    The set_correlation_id function should set a new uuid4
    """

    # Mocks the fast-api-context class
    fast_api_context = MagicMock(spec_set=FastApiContext)

    # Mocks the request class
    request_mock = MagicMock(spec=Request)
    request_mock.headers = {}

    # Sets the correlation-id
    set_correlation_id(request_mock, fast_api_context)

    # Checks whether a new uuid4 correlation-id is set
    correlation_id = fast_api_context.correlation_id_var
    assert UUID(correlation_id)


def test_set_correlation_id_existing():
    """
    Tests the set_correlation_id function when an existing correlation id should be used.
    The set_correlation_id function should return an existing uuid4
    """

    # Mocks the fast-api-context class
    fast_api_context = MagicMock(spec_set=FastApiContext)

    # Mocks the request class
    request_mock = MagicMock(spec=Request)
    request_mock.headers = {"x-correlation-id": "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2"}

    # Sets the correlation-id
    set_correlation_id(request_mock, fast_api_context)

    # Checks whether an existing uuid4 correlation-id is set
    correlation_id = fast_api_context.correlation_id_var
    assert correlation_id == "a976b291-fa0e-4b65-8a9b-dcf4d94e3dd2"
