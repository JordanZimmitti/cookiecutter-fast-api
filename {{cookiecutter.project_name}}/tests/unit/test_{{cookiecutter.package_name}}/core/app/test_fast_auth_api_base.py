from unittest.mock import MagicMock

from pytest import mark

from {{cookiecutter.package_name}}.core.app import {{cookiecutter.class_name}}Base
from {{cookiecutter.package_name}}.exceptions import (
    BadRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthenticatedError,
)


@mark.asyncio
async def test_bad_request_error_handler():
    """
    Tests the bad_request_error_handler function for completion. The bad_request_error_handler
    function should return a JSONResponse without any errors
    """

    # Mocks the bad-request-error class
    bad_request_error_mock = MagicMock(spec=BadRequestError)
    bad_request_error_mock.detail = "Test bad-request-error message"
    bad_request_error_mock.status_code = 400

    # Checks whether a valid JSONResponse instance is created correctly
    json_response = await {{cookiecutter.class_name}}Base.bad_request_error_handler(None, bad_request_error_mock)
    assert json_response.body == b'{"message":"Bad Request Error: Test bad-request-error message"}'
    assert json_response.status_code == 400


@mark.asyncio
async def test_forbidden_error_handler():
    """
    Tests the forbidden_error_handler function for completion. The forbidden_error_handler
    function should return a JSONResponse without any errors
    """

    # Mocks the forbidden-error class
    forbidden_error_mock = MagicMock(spec=ForbiddenError)
    forbidden_error_mock.detail = "Test forbidden-error message"
    forbidden_error_mock.status_code = 403

    # Checks whether a valid JSONResponse instance is created correctly
    json_response = await {{cookiecutter.class_name}}Base.forbidden_error_handler(None, forbidden_error_mock)
    assert json_response.body == b'{"message":"Forbidden Error: Test forbidden-error message"}'
    assert json_response.status_code == 403


@mark.asyncio
async def test_internal_server_error_handler():
    """
    Tests the internal_server_error_handler function for completion. The
    internal_server_error_handler function should return a JSONResponse
    without any errors
    """

    # Mocks the internal-server-error class
    internal_server_error_mock = MagicMock(spec=InternalServerError)
    internal_server_error_mock.detail = "Test internal-server-error message"
    internal_server_error_mock.status_code = 500

    # Checks whether a valid JSONResponse instance is created correctly
    json_response = await {{cookiecutter.class_name}}Base.internal_server_error_handler(
        None, internal_server_error_mock
    )
    assert json_response.body == (
        b'{"message":"Internal Server Error: Test internal-server-error message"}'
    )
    assert json_response.status_code == 500


@mark.asyncio
async def test_not_found_error_handler():
    """
    Tests the not_found_error_handler function for completion. The not_found_error_handler
    function should return a JSONResponse without any errors
    """

    # Mocks the not-found-error class
    not_found_error_mock = MagicMock(spec=NotFoundError)
    not_found_error_mock.detail = "Test not-found-error message"
    not_found_error_mock.status_code = 404

    # Checks whether a valid JSONResponse instance is created correctly
    json_response = await {{cookiecutter.class_name}}Base.not_found_error_handler(None, not_found_error_mock)
    assert json_response.body == b'{"message":"Not Found Error: Test not-found-error message"}'
    assert json_response.status_code == 404


@mark.asyncio
async def test_unauthenticated_error_handler():
    """
    Tests the unauthenticated_error_handler function for completion. The
    unauthenticated_error_handler function should return a JSONResponse
    without any errors
    """

    # Mocks the unauthenticated-error class
    unauthenticated_error_mock = MagicMock(spec=UnauthenticatedError)
    unauthenticated_error_mock.detail = "Test unauthenticated-error message"
    unauthenticated_error_mock.status_code = 401

    # Checks whether a valid JSONResponse instance is created correctly
    json_response = await {{cookiecutter.class_name}}Base.unauthenticated_error_handler(
        None, unauthenticated_error_mock
    )
    assert json_response.body == (
        b'{"message":"Unauthenticated Error: Test unauthenticated-error message"}'
    )
    assert json_response.status_code == 401
