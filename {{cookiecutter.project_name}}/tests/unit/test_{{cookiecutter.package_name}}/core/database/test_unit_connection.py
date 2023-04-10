from unittest.mock import MagicMock

from pydantic import SecretStr
from pytest import mark, raises
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.core.database import connection
from {{cookiecutter.package_name}}.core.database.connection import DatabaseConnection
from {{cookiecutter.package_name}}.exceptions import InternalServerError


def test_connect(mocker):
    """
    Tests the connect function for completion. The connection
    function should run without and errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the db-connection class
    db_connection_mock = MagicMock(spec=DatabaseConnection)
    db_connection_mock._db_uri = SecretStr("")
    db_connection_mock._display_name = ""

    # Mocks and overrides the create_async_engine function
    engine_mock = MagicMock(spec_set=AsyncEngine)
    mocker.patch.object(connection, "create_async_engine", return_value=engine_mock)

    # Mocks and overrides the async_sessionmaker function
    session_maker_mock = MagicMock(spec_set=async_sessionmaker[AsyncSession])
    mocker.patch.object(connection, "async_sessionmaker", return_value=session_maker_mock)

    # Checks whether the connection function runs without any errors
    DatabaseConnection.connect(self=db_connection_mock)
    assert db_connection_mock._engine == engine_mock
    assert db_connection_mock._session_maker == session_maker_mock


@mark.asyncio
async def test_disconnect(mocker):
    """
    Tests the disconnect function for completion. The disconnect
    function should run without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the db-connection class
    db_connection_mock = MagicMock(spec=DatabaseConnection)
    db_connection_mock._display_name = ""
    db_connection_mock._engine = MagicMock(spec_set=AsyncEngine)

    # Overrides the close_all_sessions function
    mocker.patch.object(connection, "close_all_sessions", MagicMock())

    # Invokes the database-connection disconnect function
    await DatabaseConnection.disconnect(self=db_connection_mock)

    # Checks whether the required methods were called correctly
    assert db_connection_mock._engine.dispose.call_count == 1


def test_get_engine(mocker):
    """
    Tests the engine property for completion. The
    engine property should return an engine
    """

    # Mocks and overrides the create_async_engine function
    async_engine_mock = MagicMock(spec_set=AsyncEngine)
    mocker.patch.object(connection, "create_async_engine", return_value=async_engine_mock)

    # Overrides the async sessionmaker function
    mocker.patch.object(connection, "async_sessionmaker", MagicMock())

    # Creates a db-connection instance
    db_connection = DatabaseConnection(
        display_name="test-display-name", db_uri=SecretStr("test-db-uri")
    )
    db_connection.connect()

    # Checks whether the engine was retrieved correctly
    engine = db_connection.engine
    assert engine == async_engine_mock


def test_get_engine_before_connect():
    """
    Tests the engine property when no database is connected. The
    engine property should raise an InternalServerError
    """

    # Creates a db-connection instance
    db_connection = DatabaseConnection(
        display_name="test-display-name", db_uri=SecretStr("test-db-uri")
    )

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        _ = db_connection.engine


def test_get_session_maker(mocker):
    """
    Tests the session_maker property for completion. The
    session_maker property should return a session_maker

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks and overrides the create_async_engine function
    engine_mock = MagicMock(spec_set=AsyncEngine)
    mocker.patch.object(connection, "create_async_engine", return_value=engine_mock)

    # Mocks and overrides the async_sessionmaker function
    session_maker_mock = MagicMock(spec_set=async_sessionmaker[AsyncSession])
    mocker.patch.object(connection, "async_sessionmaker", return_value=session_maker_mock)

    # Creates a db-connection instance
    db_connection = DatabaseConnection(
        display_name="test-display-name", db_uri=SecretStr("test-db-uri")
    )
    db_connection.connect()

    # Checks whether the session-maker was retrieved correctly
    session_maker = db_connection.session_maker
    assert session_maker == session_maker_mock


def test_get_session_maker_before_connect():
    """
    Tests the session_maker property when no database is connected.
    The session_maker property should raise an InternalServerError
    """

    # Creates a db-connection instance
    db_connection = DatabaseConnection(
        display_name="test-display-name", db_uri=SecretStr("test-db-uri")
    )

    # Checks whether the correct error was raised
    with raises(InternalServerError):
        db_connection.session_maker()


def test_init():
    """
    Tests the DatabaseConnection init function for completion. The DatabaseConnection
    init function should instantiate a DatabaseConnection instance without any errors
    """

    # Define and instantiates the database-connection class
    db_connection = DatabaseConnection(
        display_name="test-display-name",
        db_uri=SecretStr("test-db-uri"),
    )

    # Checks whether the database-connection class correctly instantiated
    assert db_connection._display_name == "test-display-name"
    assert db_connection._db_uri == SecretStr("test-db-uri")
