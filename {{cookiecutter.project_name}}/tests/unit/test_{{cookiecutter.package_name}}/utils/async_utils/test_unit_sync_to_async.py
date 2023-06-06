from asyncio import AbstractEventLoop
from unittest.mock import AsyncMock, MagicMock

from pytest import mark

from {{cookiecutter.package_name}}.utils.async_utils import run_sync_function, sync_to_async


@mark.asyncio
async def test_run_sync_function(mocker):
    """
    Mocks the run_sync_function function for completion. The run_sync_function function
    should run a synchronous function asynchronously without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the run_in_executor function
    run_in_executor_mock = AsyncMock()
    run_in_executor_mock.return_value = "return-value"

    # Mocks the abstract-event-loop class
    abstract_event_loop_mock = MagicMock(spec_set=AbstractEventLoop)
    abstract_event_loop_mock.run_in_executor = run_in_executor_mock

    # Mocks and overrides the get_running_loop function
    get_running_loop_mock = MagicMock()
    get_running_loop_mock.return_value = abstract_event_loop_mock
    mocker.patch.object(sync_to_async, "get_running_loop", get_running_loop_mock)

    # Mocks a synchronous function
    sync_function_mock = MagicMock()

    # Invokes the run_sync_function function
    result = await run_sync_function(sync_function_mock, "arg")

    # Checks whether the synchronous function ran asynchronously
    assert result == "return-value"
    assert get_running_loop_mock.called
    assert run_in_executor_mock.called
    assert run_in_executor_mock.call_args.args[0] is None
    assert run_in_executor_mock.call_args.args[1] == sync_function_mock
    assert run_in_executor_mock.call_args.args[2] == "arg"
