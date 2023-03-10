from asyncio import AbstractEventLoop, get_event_loop_policy
from os import listdir, remove
from os.path import dirname, exists, join, pardir
from typing import Any, Dict, Generator
from unittest.mock import AsyncMock

from dotenv import load_dotenv
from fastapi import FastAPI
from pytest_asyncio import fixture
from starlette.testclient import TestClient

# Loads environment variables
parent_directory = join(dirname(__file__), pardir)
pytest_env_directory = join(parent_directory, "pytest.env")
load_dotenv(pytest_env_directory)


@fixture(scope="session", autouse=True)
def cleanup() -> Generator[None, Any, None]:
    """
    Pytest fixture that cleans up generated files
    and folders created during testing
    """

    # Yield nothing, waits for testing to finish
    yield None

    # Import packages after pytest environment variables are loaded
    from {{cookiecutter.package_name}}.core.settings import settings
    from {{cookiecutter.package_name}}.utils.modules.path_extensions import get_parent_path_by_file

    # Removes the application log file
    project_path = f"{get_parent_path_by_file('pyproject.toml')}"
    log_directory = f"{project_path}/{settings.LOG_FILE_DIRECTORY}/"
    if exists(log_directory):
        for file in listdir(log_directory):
            remove(join(log_directory, file))


@fixture(scope="session")
def app() -> FastAPI:
    """
    Function that creates the {{cookiecutter.friendly_name}}
    app instance

    :return: The {{cookiecutter.friendly_name}} app instance
    """

    # Import {{cookiecutter.friendly_name}} dependencies after pytest environment settings are loaded
    from {{cookiecutter.package_name}}.core.settings import settings
    from {{cookiecutter.package_name}}.main import {{cookiecutter.class_name}}

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

    # Creates the {{cookiecutter.project_name}} app instance
    api = {{cookiecutter.class_name}}(options).load()
    return api


@fixture(scope="function")
def client(app) -> TestClient:
    """
    Pytest fixture that creates an {{cookiecutter.friendly_name}}
    test client for testing api requests
    """

    # Import {{cookiecutter.friendly_name}} dependencies after pytest environment settings are loaded
    from {{cookiecutter.package_name}}.core.cache import get_fast_api_context

    # Yields the Fast-Auth API test client
    with TestClient(app) as test_client:

        # Saves the fast-api-context into the app state
        fast_api_context = get_fast_api_context()
        test_client.app.state.fast_api_context = fast_api_context

        # Adds a mock database and redis managers into the app state
        test_client.app.state.db_manager = AsyncMock()
        test_client.app.state.redis_manager = AsyncMock()

        # Returns the client instance
        yield test_client


@fixture(scope="function")
def dependency_overrides(app) -> Dict:
    """
    Pytest fixture that gets the fast-api dependency overrides dict
    for overriding certain route dependencies while testing
    """

    # Yields the fast-api dependency overrides dict
    yield app.dependency_overrides

    # Clears dependency overrides for the next test
    app.dependency_overrides.clear()


@fixture(scope="session", autouse=True)
def event_loop() -> Generator[AbstractEventLoop, Any, None]:
    """
    Pytest fixture that creates an event-loop
    for asynchronous operations

    :return: The new event loop
    """

    # Returns the newly started event-loop
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
