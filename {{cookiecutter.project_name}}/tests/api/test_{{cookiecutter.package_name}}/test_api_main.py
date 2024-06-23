from unittest.mock import AsyncMock

from pydantic import BaseModel, Field
from starlette.testclient import TestClient

from {{cookiecutter.package_name}} import main
from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.exceptions import ForbiddenError, UnauthenticatedError
from tests.mocks import async_error_mock

# Gunicorn options
options = {
    "bind": f"0.0.0.0:{settings.LISTEN_PORT}",
    "workers": settings.UVICORN_CONCURRENCY,
    "worker_class": "uvicorn.workers.UvicornWorker",
    "worker_connections": settings.UVICORN_CONNECTIONS,
    "max_requests": settings.UVICORN_MAX_REQUESTS,
    "max_requests_jitter": settings.UVICORN_MAX_REQUESTS_JITTER,
    "timeout": settings.UVICORN_TIMEOUT,
}


def test_main_{{cookiecutter.package_name}}_forbidden_error(mocker, client: TestClient):
    """
    Tests the {{cookiecutter.friendly_name}} class when an ForbiddenError occurs. The
    {{cookiecutter.friendly_name}} should return the correct error message

    :param mocker: Fixture to mock specific functions for testing
    :param client: A test client for hitting {{cookiecutter.friendly_name}} http requests
    """

    # Overrides the handle_request function
    error = ForbiddenError("error")
    mocker.patch.object(main, "handle_request", AsyncMock(side_effect=error))

    # Hits the default {{cookiecutter.friendly_name}} endpoint
    response = client.get("/")

    # Checks whether the response was retrieved correctly
    assert response.status_code == 403

    # Checks whether the correct message response was returned
    data = response.json()
    error_message = "Forbidden Error: error"
    assert data.get("message") == error_message


def test_main_{{cookiecutter.package_name}}_middleware_error(mocker, client: TestClient):
    """
    Tests the {{cookiecutter.friendly_name}} class when a middleware error occurs. The
    {{cookiecutter.friendly_name}} should return the correct error message

    :param mocker: Fixture to mock specific functions for testing
    :param client: A test client for hitting {{cookiecutter.friendly_name}} http requests
    """

    # Overrides the handle_request function
    mocker.patch.object(main, "handle_request", async_error_mock)

    # Hits the default {{cookiecutter.friendly_name}} endpoint
    response = client.get("/")

    # Checks whether the response was retrieved correctly
    assert response.status_code == 500

    # Checks whether the correct message response was returned
    data = response.json()
    error_message = "Internal Server Error: An unexpected error occurred, please try again"
    assert data.get("message") == error_message


def test_main_{{cookiecutter.package_name}}_redirect(client: TestClient):
    """
    Tests the default {{cookiecutter.friendly_name}} endpoint. The default {{cookiecutter.friendly_name}}
    endpoint should redirect to the swagger-ui docs without any errors

    :param client: A test client for hitting {{cookiecutter.friendly_name}} server http requests
    """

    # Hits the default {{cookiecutter.friendly_name}} endpoint
    response = client.get("/")

    # Checks whether the response was retrieved correctly
    assert response.status_code == 200

    # Checks whether the redirect to the swagger-ui docs was successful
    assert b"swagger-ui" in response.content


def test_main_{{cookiecutter.package_name}}_unauthenticated_error(mocker, client: TestClient):
    """
    Tests the {{cookiecutter.friendly_name}} class when an UnauthenticatedError occurs. The
    {{cookiecutter.friendly_name}} should return the correct error message

    :param mocker: Fixture to mock specific functions for testing
    :param client: A test client for hitting {{cookiecutter.friendly_name}} http requests
    """

    # Overrides the handle_request function
    error = UnauthenticatedError("error")
    mocker.patch.object(main, "handle_request", AsyncMock(side_effect=error))

    # Hits the default {{cookiecutter.friendly_name}} endpoint
    response = client.get("/")

    # Checks whether the response was retrieved correctly
    assert response.status_code == 401

    # Checks whether the correct message response was returned
    data = response.json()
    error_message = "Unauthenticated Error: error"
    assert data.get("message") == error_message


def test_main_{{cookiecutter.package_name}}_validation_error(mocker, client: TestClient):
    """
    Tests the {{cookiecutter.friendly_name}} class when a middleware error occurs. The
    {{cookiecutter.friendly_name}} should return the correct error message

    :param mocker: Fixture to mock specific functions for testing
    :param client: A test client for hitting {{cookiecutter.friendly_name}} http requests
    """

    # Function that raises a pydantic validation error
    def raise_validation_error(_, __, ___):
        class Model(BaseModel):
            x: str = Field(min_length=1)

        Model(x="")

    # Overrides the handle_request function
    mocker.patch.object(main, "handle_request", AsyncMock(side_effect=raise_validation_error))

    # Hits the default {{cookiecutter.friendly_name}} endpoint
    response = client.get("/")

    # Checks whether the response was retrieved correctly
    assert response.status_code == 422
