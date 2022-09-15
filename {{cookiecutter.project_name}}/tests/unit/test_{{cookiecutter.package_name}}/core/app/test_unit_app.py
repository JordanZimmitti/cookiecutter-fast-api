from unittest.mock import AsyncMock, MagicMock

from fastapi import FastAPI, Request, Response
from prometheus_fastapi_instrumentator import Instrumentator
from pytest import mark

from {{cookiecutter.package_name}}.core.app import (
    app,
    deconstruct_app_state,
    expose_metrics_endpoint,
    handle_request,
    setup_app,
    setup_app_state,
)
from {{cookiecutter.package_name}}.core.cache import FastApiContext
from {{cookiecutter.package_name}}.core.database import DatabaseManager


@mark.asyncio
async def test_deconstruct_app_state():
    """
    Tests the deconstruct_app_state function for completion. The deconstruct_app_state function
    should run without any errors
    """

    # Mocks the fast-api class
    app_mock = MagicMock(spec=FastAPI)
    app_mock.state = MagicMock()

    # Mocks the fast-api-context class
    app_mock.state.fast_api_context = MagicMock(spec_set=FastApiContext)

    # Mocks the database-manager class
    db_manager_mock = MagicMock(spec_set=DatabaseManager)
    db_manager_mock.connection.disconnect = AsyncMock()
    app_mock.state.db_manager = db_manager_mock

    # Invokes the deconstruct_app_state function
    await deconstruct_app_state(app_mock)

    # Checks whether the required methods were called correctly
    assert app_mock.state.db_manager.connection.disconnect.call_count == 1
    assert app_mock.state.fast_api_context.reset.call_count == 1


def test_expose_metrics_endpoint(mocker):
    """
    Tests the expose_metrics_endpoint function for completion. The expose_metrics_endpoint
    function should run to completion without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the fast-api class
    app_mock = MagicMock(spec_set=FastAPI)

    # Mocks and overrides the instrumentator class
    instrumentator_mock = MagicMock(spec_set=Instrumentator)
    mocker.patch.object(app, "Instrumentator", return_value=instrumentator_mock)

    # Invokes the expose_metrics_endpoint function
    expose_metrics_endpoint(app_mock)

    # Checks whether both instrumentator functions were called
    assert instrumentator_mock.expose.called
    assert instrumentator_mock.instrument.called


@mark.asyncio
async def test_handle_request(mocker):
    """
    Tests the handle_request function for completion. The handle_request function
    should return a response with a valid 200 http status_code

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the fast-api class
    app_mock = MagicMock(spec=FastAPI)
    app_mock.state = MagicMock()

    # Mocks the request class
    request_mock = MagicMock(spec=Request)

    # Mocks the call_next function
    async def call_next_mock(*_):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        return response_mock

    # Overrides the get_request_metadata function
    mocker.patch.object(
        app,
        "get_request_metadata",
        return_value=("GET", "https://test-url", {"user-agent": "test-agent"}),
    )

    # Overrides the set_correlation_id function
    mocker.patch.object(app, "set_correlation_id", MagicMock())

    # Checks whether the response was retrieved correctly
    response = await handle_request(app_mock, request_mock, call_next_mock)
    assert response.status_code == 200


def test_setup_app():
    """
    Tests the setup_app function for completion. The setup_app
    function should run to completion without any errors
    """

    # Mocks the fast-api class
    app_mock = MagicMock(spec=FastAPI)

    # Invokes the setup_app function
    setup_app(app_mock)

    # Checks whether the include_router function was invoked
    assert app_mock.include_router.called


def test_setup_app_state(mocker):
    """
    Tests the setup_app_state function for completion. The setup_app_state function
    should run without any errors
    """

    # Mocks the fast-api class
    app_mock = MagicMock(spec=FastAPI)
    app_mock.state = MagicMock()

    # Mocks and overrides the db-manager class
    db_manager_mock = MagicMock(spec_set=DatabaseManager)
    mocker.patch.object(app, "DatabaseManager", return_value=db_manager_mock)

    # Mocks and overrides the get_fast_api_context function
    fast_api_context_mock = MagicMock(spec_set=FastApiContext)
    mocker.patch.object(app, "get_fast_api_context", return_value=fast_api_context_mock)

    # Checks whether the setup_app_state function runs without any errors
    setup_app_state(app_mock)
    assert app_mock.state.db_manager == db_manager_mock
    assert app_mock.state.db_manager.connection.connect.called
    assert app_mock.state.fast_api_context == fast_api_context_mock
