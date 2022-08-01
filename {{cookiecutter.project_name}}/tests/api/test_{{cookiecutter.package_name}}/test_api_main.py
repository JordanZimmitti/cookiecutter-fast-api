from typing import Any, Dict

from fastapi import FastAPI
from pytest import mark
from starlette.testclient import TestClient

from {{cookiecutter.package_name}} import main
from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.main import {{cookiecutter.class_name}}
from tests.mocks import error_mock

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


def test_main_{{cookiecutter.package_name}}_load():
    """
    Tests the {{cookiecutter.friendly_name}} class for completion. The {{cookiecutter.friendly_name}} class
    should return the {{cookiecutter.friendly_name}} app instance without any errors
    """

    # Gets the {{cookiecutter.friendly_name}} fast-api app instance
    app = {{cookiecutter.class_name}}(options).load()

    # Checks whether the fast-api app instance was returned
    assert isinstance(app, FastAPI)


def test_main_{{cookiecutter.package_name}}_middleware_error(mocker, client: TestClient):
    """
    Tests the {{cookiecutter.friendly_name}} class when a middleware error occurs. The
    {{cookiecutter.friendly_name}} should return the correct error message

    :param mocker: Fixture to mock specific functions for testing
    :param client: A test client for hitting {{cookiecutter.friendly_name}} http requests
    """

    # Mocks the handle_request function
    mocker.patch.object(main, "handle_request", error_mock)

    # Hits the default {{cookiecutter.friendly_name}} endpoint
    response = client.get("/")

    # Checks whether the response was retrieved correctly
    assert response.status_code == 500

    # Checks whether the correct message response was returned
    data = response.json()
    assert data.get("message") == "Middleware Error: mock error"


def test_main_{{cookiecutter.package_name}}_open_api(client: TestClient):
    """
    Tests the default {{cookiecutter.friendly_name}} endpoint. The default {{cookiecutter.friendly_name}}
    endpoint should redirect to the swagger-ui docs without any errors

    :param client: A test client for hitting {{cookiecutter.friendly_name}} http requests
    """

    # Hits the default {{cookiecutter.friendly_name}} endpoint
    response = client.get(f"{settings.API_PREFIX}/openapi.json")

    # Checks whether the response was retrieved correctly
    assert response.status_code == 200

    # Gets the open-api data
    open_api: Dict[str, Any] = response.json()

    # Checks whether the correct open-api data exists
    assert open_api.get("openapi") == "3.0.2"

    # Hits the default {{cookiecutter.friendly_name}} endpoint
    response = client.get(f"{settings.API_PREFIX}/openapi.json")

    # Checks whether the response was retrieved correctly
    assert response.status_code == 200

    # Gets the open-api data
    open_api: Dict[str, Any] = response.json()

    # Checks whether the correct open-api data exists
    assert open_api.get("openapi") == "3.0.2"


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


@mark.asyncio
async def test_main_{{cookiecutter.package_name}}_startup_and_shutdown():
    """
    Tests the {{cookiecutter.friendly_name}} class startup and shutdown function. The startup
    and shutdown function should run to completion without any errors
    """

    # Gets the h API FastAPI app instance
    await {{cookiecutter.class_name}}(options).startup()
    await {{cookiecutter.class_name}}(options).shutdown()
