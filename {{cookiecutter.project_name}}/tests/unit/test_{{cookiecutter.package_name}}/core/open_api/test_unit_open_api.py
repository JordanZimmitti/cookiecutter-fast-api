from unittest.mock import MagicMock

from fastapi import FastAPI

from {{cookiecutter.package_name}}.core.open_api import get_open_api_instance, open_api
from tests.mocks import get_openapi_mock


def test_get_open_api_instance_exists():
    """
    Tests the get_open_api_instance function when the open api instance already exists.
    The get_open_api_instance function should return the existing open-api instance
    """

    # Mocks the fast-api class
    app_mock = MagicMock(spec=FastAPI)
    app_mock.openapi_schema = get_openapi_mock()

    # Get the open-api instance that already exists
    open_api_instance = get_open_api_instance(app_mock)

    # Checks whether the open-api instance was retrieved correctly
    assert open_api_instance == app_mock.openapi_schema


def test_get_open_api_instance_not_exists(mocker):
    """
    Tests the get_open_api_instance function when the open api instance does not exist.
    The get_open_api_instance function should return the new open-api instance

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the fast-api class
    app_mock = MagicMock(spec=FastAPI)
    app_mock.openapi_schema = None
    app_mock.routes = None

    # Overrides the get_openapi function
    mocker.patch.object(open_api, "get_openapi", get_openapi_mock)

    # Get the open-api instance when a new one is created
    get_open_api_instance(app_mock)

    # Checks whether the open-api instance was created correctly
    assert app_mock.openapi_schema == get_openapi_mock()
