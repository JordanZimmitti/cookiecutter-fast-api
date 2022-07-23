from {{cookiecutter.package_name}}.exceptions import (
    BadRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthenticatedError,
)


def test_bad_request_error():
    """
    Tests the BadRequestError class for completion. The BadRequestError class
    should instantiate without any errors
    """

    # Creates the test error message
    error_message = "Test bad-request-error message"

    # Checks whether the BadRequestError class was instantiated correctly
    bad_request_error = BadRequestError(error_message)
    assert bad_request_error.status_code == 400
    assert bad_request_error.detail == error_message


def test_forbidden_error():
    """
    Tests the ForbiddenError class for completion. The ForbiddenError class
    should instantiate without any errors
    """

    # Creates the test error message
    error_message = "Test forbidden-error message"

    # Checks whether the ForbiddenError class was instantiated correctly
    forbidden_error = ForbiddenError(error_message)
    assert forbidden_error.status_code == 403
    assert forbidden_error.detail == error_message


def test_internal_server_error():
    """
    Tests the InternalServerError class for completion. The InternalServerError class
    should instantiate without any errors
    """

    # Creates the test error message
    error_message = "Test internal-server-error message"

    # Checks whether the InternalServerError class was instantiated correctly
    internal_server_error = InternalServerError(error_message)
    assert internal_server_error.status_code == 500
    assert internal_server_error.detail == error_message


def test_not_found_error():
    """
    Tests the NotFoundError class for completion. The NotFoundError class
    should instantiate without any errors
    """

    # Creates the test error message
    error_message = "Test not-found-error message"

    # Checks whether the NotFoundError class was instantiated correctly
    internal_server_error = NotFoundError(error_message)
    assert internal_server_error.status_code == 404
    assert internal_server_error.detail == error_message


def test_unauthenticated_error():
    """
    Tests the UnauthenticatedError class for completion. The UnauthenticatedError class
    should instantiate without any errors
    """

    # Creates the test error message
    error_message = "Test unauthenticated-error message"

    # Checks whether the UnauthenticatedError class was instantiated correctly
    unauthenticated_error = UnauthenticatedError(error_message)
    assert unauthenticated_error.status_code == 401
    assert unauthenticated_error.detail == error_message
