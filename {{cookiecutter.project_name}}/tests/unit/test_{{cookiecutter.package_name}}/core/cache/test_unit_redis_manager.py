from unittest.mock import AsyncMock, MagicMock

from pydantic import SecretStr
from pytest import mark, raises
from redis.asyncio.client import Pipeline, Redis

from {{cookiecutter.package_name}}.core.cache import RedisManager, redis_manager
from {{cookiecutter.package_name}}.core.settings import Settings
from {{cookiecutter.package_name}}.exceptions import InternalServerError


def test_connect(mocker):
    """
    Tests the connect function for completion. The connection
    function should run without and errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks and overrides the redis class
    redis_mock = MagicMock(spec_set=Redis)
    redis_mock.return_value = redis_mock
    mocker.patch.object(redis_manager, "Redis", redis_mock)

    # Mocks the redis-manager class
    redis_manager_mock = MagicMock(spec=RedisManager)
    redis_manager_mock._host = SecretStr("test-host")
    redis_manager_mock._port = SecretStr("1234")
    redis_manager_mock._password = SecretStr("test-password")
    redis_manager_mock._display_name = "test-name"

    # Mocks the redis-manager class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_REDIS_DECODE_RESPONSES = True
    mocker.patch.object(redis_manager, "settings", settings_mock)

    # Checks whether the connection function runs without any errors
    RedisManager.connect(self=redis_manager_mock)
    assert redis_manager_mock._operation == redis_mock
    assert redis_mock.called
    assert redis_mock.call_args.kwargs == {
        "host": "test-host",
        "port": 1234,
        "password": "test-password",
        "decode_responses": True,
    }


@mark.asyncio
async def test_disconnect():
    """
    Tests the disconnect function for completion. The disconnect
    function should run without and errors
    """

    # Mocks and overrides the redis class
    redis_mock = MagicMock(spec_set=Redis)

    # Mocks the redis-manager class
    redis_manager_mock = MagicMock(spec=RedisManager)
    redis_manager_mock._display_name = "test-name"
    redis_manager_mock._operation = redis_mock

    await RedisManager.disconnect(self=redis_manager_mock)
    assert redis_mock.close.called


def test_get_description():
    """
    Tests the description property for completion. The
    description property should return a description
    """

    # Creates the redis-manager instance
    redis_manager_instance = RedisManager(
        display_name="test-name",
        description="test-description",
        host=SecretStr("test-host"),
        port=SecretStr("test-port"),
        password=SecretStr("test-password"),
    )

    # Checks whether the description was retrieved correctly
    description = redis_manager_instance.description
    assert description == "test-description"


def test_get_display_name():
    """
    Tests the display_name property for completion. The
    display_name property should return a display_name
    """

    # Creates the redis-manager instance
    redis_manager_instance = RedisManager(
        display_name="test-name",
        description="test-description",
        host=SecretStr("test-host"),
        port=SecretStr("test-port"),
        password=SecretStr("test-password"),
    )

    # Checks whether the display-name was retrieved correctly
    display_name = redis_manager_instance.display_name
    assert display_name == "test-name"


def test_init():
    """
    Tests the RedisManager init function for completion. The RedisManager init
    function should instantiate a RedisManager instance without any errors
    """

    # Define and instantiates the redis-manager class
    redis_manager_instance = RedisManager(
        display_name="test-display-name",
        description="test-description",
        host=SecretStr("test-host"),
        port=SecretStr("test-port"),
        password=SecretStr("test-password"),
    )

    # Checks whether the redis-manager class correctly instantiated
    assert redis_manager_instance._display_name == "test-display-name"
    assert redis_manager_instance._description == "test-description"
    assert redis_manager_instance._host == SecretStr("test-host")
    assert redis_manager_instance._port == SecretStr("test-port")
    assert redis_manager_instance._password == SecretStr("test-password")
    assert redis_manager_instance._operation is None


def test_get_operation():
    """
    Tests the operation property for completion. The
    operation property should return an operation
    """

    # Mocks the redis class
    operation_mock = MagicMock(spec_set=Redis)

    # Creates the redis-manager instance
    redis_manager_instance = RedisManager(
        display_name="test-name",
        description="test-description",
        host=SecretStr("test-host"),
        port=SecretStr("test-port"),
        password=SecretStr("test-password"),
    )
    redis_manager_instance._operation = operation_mock

    # Checks whether the display-name was retrieved correctly
    operation = redis_manager_instance.operation
    assert operation == operation_mock


def test_get_operation_no_operation():
    """
    Tests the operation property when no operation exists. The
    operation property should raise an InternalServerError()
    """

    # Creates the redis-manager instance
    redis_manager_instance = RedisManager(
        display_name="test-name",
        description="test-description",
        host=SecretStr("test-host"),
        port=SecretStr("test-port"),
        password=SecretStr("test-password"),
    )

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        assert redis_manager_instance.operation


@mark.asyncio
async def test_pipeline():
    """
    Tests the RedisManager pipeline function for completion. The RedisManager
    pipeline class should return a result without any errors
    """

    # Mocks the pipeline class
    pipe_mock = AsyncMock(spec_set=Pipeline)
    pipe_mock.execute.return_value = ["result"]

    # Mocks the redis class
    operation_mock = MagicMock(spec_set=Redis)
    operation_mock.pipeline.return_value.__aenter__.return_value = pipe_mock

    # Mocks the redis-manager class
    redis_manager_mock = MagicMock(spec=RedisManager)
    redis_manager_mock._operation = operation_mock

    # Mocks the pipe_ops function
    pipe_ops_mock = MagicMock()

    # Invokes the redis-manager pipeline class
    result = await RedisManager.pipeline.__wrapped__.__wrapped__(
        self=redis_manager_mock, pipe_ops=pipe_ops_mock
    )

    # Checks whether the result was retrieved correctly
    assert result == ["result"]
    assert operation_mock.pipeline.called
    assert operation_mock.pipeline.call_args.args[0] is True
    assert pipe_ops_mock.called
    assert pipe_ops_mock.call_args.args[0] == pipe_mock
    assert pipe_mock.execute.called


@mark.asyncio
async def test_pipeline_scalar():
    """
    Tests the RedisManager pipeline function when a scalar is expected.
    The RedisManager pipeline class should return a scalar result
    """

    # Mocks the pipeline class
    pipe_mock = AsyncMock(spec_set=Pipeline)
    pipe_mock.execute.return_value = ["result"]

    # Mocks the redis class
    operation_mock = MagicMock(spec_set=Redis)
    operation_mock.pipeline.return_value.__aenter__.return_value = pipe_mock

    # Mocks the redis-manager class
    redis_manager_mock = MagicMock(spec=RedisManager)
    redis_manager_mock._operation = operation_mock

    # Mocks the pipe_ops function
    pipe_ops_mock = MagicMock()

    # Invokes the redis-manager pipeline class
    result = await RedisManager.pipeline.__wrapped__.__wrapped__(
        self=redis_manager_mock, pipe_ops=pipe_ops_mock, is_scalar=True
    )

    # Checks whether the result was retrieved correctly
    assert result == "result"
    assert operation_mock.pipeline.called
    assert operation_mock.pipeline.call_args.args[0] is True
    assert pipe_ops_mock.called
    assert pipe_ops_mock.call_args.args[0] == pipe_mock
    assert pipe_mock.execute.called


@mark.asyncio
async def test_pipeline_error():
    """
    Tests the RedisManager pipeline function when an error occurs. The
    RedisManager pipeline class should raise an InternalServerError
    """

    # Mocks the pipeline class
    pipe_mock = AsyncMock(spec_set=Pipeline)

    # Mocks the redis class
    operation_mock = MagicMock(spec_set=Redis)
    operation_mock.pipeline.return_value.__aenter__.return_value = pipe_mock

    # Mocks the redis-manager class
    redis_manager_mock = MagicMock(spec=RedisManager)
    redis_manager_mock._operation = operation_mock

    # Mocks the pipe_ops function
    pipe_ops_mock = MagicMock(side_effect=InternalServerError())

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        await RedisManager.pipeline.__wrapped__.__wrapped__(
            self=redis_manager_mock, pipe_ops=pipe_ops_mock
        )

    # Checks whether the result was retrieved correctly
    assert operation_mock.pipeline.called
    assert operation_mock.pipeline.call_args.args[0] is True
    assert pipe_ops_mock.called
    assert pipe_ops_mock.call_args.args[0] == pipe_mock
