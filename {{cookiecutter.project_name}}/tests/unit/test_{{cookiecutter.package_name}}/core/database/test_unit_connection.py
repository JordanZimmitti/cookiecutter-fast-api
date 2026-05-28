from unittest.mock import AsyncMock, MagicMock

from google.cloud.sql.connector import Connector, IPTypes
from pydantic import SecretStr
from pytest import raises
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.core.database import connection
from {{cookiecutter.package_name}}.core.database.connection import DatabaseConnection
from {{cookiecutter.package_name}}.core.settings import Settings
from {{cookiecutter.package_name}}.exceptions import InternalServerError


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
    assert db_connection._connector is None
    assert db_connection._engine is None
    assert db_connection._session_maker is None


async def test_engine(mocker):
    """
    Tests the engine property for completion. The
    engine property should return an engine

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_DB_TYPE = "native"
    settings_mock.IS_ECHO_SQLALCHEMY_LOGS = False
    settings_mock.PROJECT_NAME = "project-name"
    settings_mock.SQLALCHEMY_MAX_OVERFLOW = 2
    settings_mock.SQLALCHEMY_POOL_SIZE = 1
    settings_mock.SQLALCHEMY_POOL_TIMEOUT = 10
    mocker.patch.object(connection, "settings", settings_mock)

    # Mocks and overrides the create_async_engine function
    async_engine_mock = MagicMock(spec_set=AsyncEngine)
    mocker.patch.object(connection, "create_async_engine", return_value=async_engine_mock)

    # Overrides the async sessionmaker function
    mocker.patch.object(connection, "async_sessionmaker", MagicMock())

    # Creates a db-connection instance
    db_connection = DatabaseConnection(
        display_name="test-display-name", db_uri=SecretStr("test-db-uri")
    )
    await db_connection.connect()

    # Checks whether the engine was retrieved correctly
    engine = db_connection.engine
    assert engine == async_engine_mock


def test_engine_before_connect():
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


async def test_get_session_maker(mocker):
    """
    Tests the session_maker property for completion. The
    session_maker property should return a session_maker

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_DB_TYPE = "native"
    settings_mock.IS_ECHO_SQLALCHEMY_LOGS = False
    settings_mock.PROJECT_NAME = "project-name"
    settings_mock.SQLALCHEMY_MAX_OVERFLOW = 2
    settings_mock.SQLALCHEMY_POOL_SIZE = 1
    settings_mock.SQLALCHEMY_POOL_TIMEOUT = 10
    mocker.patch.object(connection, "settings", settings_mock)

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
    await db_connection.connect()

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


async def test_connect(mocker):
    """
    Tests the connect function for completion. The connection
    function should run without and errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_DB_TYPE = "native"
    settings_mock.IS_ECHO_SQLALCHEMY_LOGS = False
    settings_mock.PROJECT_NAME = "project-name"
    settings_mock.SQLALCHEMY_MAX_OVERFLOW = 2
    settings_mock.SQLALCHEMY_POOL_SIZE = 1
    settings_mock.SQLALCHEMY_POOL_TIMEOUT = 10
    mocker.patch.object(connection, "settings", settings_mock)

    # Mock and overrides the create_async_connector function
    create_async_connector_mock = AsyncMock()
    create_async_connector_mock.return_value = create_async_connector_mock
    mocker.patch.object(connection, "create_async_connector", create_async_connector_mock)

    # Mock and overrides the create_async_engine function
    create_async_engine_mock = MagicMock()
    create_async_engine_mock.return_value = create_async_engine_mock
    mocker.patch.object(connection, "create_async_engine", create_async_engine_mock)

    # Mock and overrides the async_sessionmaker function
    async_sessionmaker_mock = MagicMock()
    async_sessionmaker_mock.return_value = async_sessionmaker_mock
    mocker.patch.object(connection, "async_sessionmaker", async_sessionmaker_mock)

    # Mocks the database-connection class
    database_connection_mock = MagicMock(spec=DatabaseConnection)
    database_connection_mock._display_name = "display-name"
    database_connection_mock._db_uri = SecretStr("db-uri")

    # Invokes the connect function
    await DatabaseConnection.connect(self=database_connection_mock)

    # Checks whether all the class variables were set correctly
    assert database_connection_mock._engine == create_async_engine_mock
    assert database_connection_mock._session_maker == async_sessionmaker_mock
    assert not create_async_connector_mock.called
    assert create_async_engine_mock.called
    assert create_async_engine_mock.call_args.kwargs == {
        "url": "db-uri",
        "async_creator": None,
        "pool_pre_ping": True,
        "pool_timeout": 10,
        "pool_size": 1,
        "max_overflow": 2,
        "echo": False,
        "connect_args": {"server_settings": {"application_name": "project-name"}},
    }
    assert async_sessionmaker_mock.called
    assert async_sessionmaker_mock.call_args.args[0] == create_async_engine_mock
    assert async_sessionmaker_mock.call_args.kwargs == {"expire_on_commit": False}


async def test_connect_cloud(mocker):
    """
    Tests the connect function when a Cloud SQL connection is made.
    The connection function should run without and errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_DB_DRIVER = SecretStr("driver")
    settings_mock.API_DB_TYPE = "cloud"
    settings_mock.IS_ECHO_SQLALCHEMY_LOGS = False
    settings_mock.PROJECT_NAME = "project-name"
    settings_mock.SQLALCHEMY_MAX_OVERFLOW = 2
    settings_mock.SQLALCHEMY_POOL_SIZE = 1
    settings_mock.SQLALCHEMY_POOL_TIMEOUT = 10
    mocker.patch.object(connection, "settings", settings_mock)

    # Mock and overrides the create_async_connector function
    create_async_connector_mock = AsyncMock()
    create_async_connector_mock.return_value = create_async_connector_mock
    mocker.patch.object(connection, "create_async_connector", create_async_connector_mock)

    # Mock and overrides the create_async_engine function
    create_async_engine_mock = MagicMock()
    create_async_engine_mock.return_value = create_async_engine_mock
    mocker.patch.object(connection, "create_async_engine", create_async_engine_mock)

    # Mock and overrides the async_sessionmaker function
    async_sessionmaker_mock = MagicMock()
    async_sessionmaker_mock.return_value = async_sessionmaker_mock
    mocker.patch.object(connection, "async_sessionmaker", async_sessionmaker_mock)

    # Mocks the database-connection class
    database_connection_mock = MagicMock(spec=DatabaseConnection)
    database_connection_mock._display_name = "display-name"
    database_connection_mock._db_uri = SecretStr("db-uri")

    # Invokes the connect function
    await DatabaseConnection.connect(self=database_connection_mock)

    # Checks whether all the class variables were set correctly
    assert database_connection_mock._connector == create_async_connector_mock
    assert database_connection_mock._engine == create_async_engine_mock
    assert database_connection_mock._session_maker == async_sessionmaker_mock
    assert create_async_connector_mock.called
    assert create_async_engine_mock.called
    assert create_async_engine_mock.call_args.kwargs == {
        "url": "driver://",
        "async_creator": database_connection_mock._get_cloud_sql_creator,
        "pool_pre_ping": True,
        "pool_timeout": 10,
        "pool_size": 1,
        "max_overflow": 2,
        "echo": False,
        "connect_args": {"server_settings": {"application_name": "project-name"}},
    }
    assert async_sessionmaker_mock.called
    assert async_sessionmaker_mock.call_args.args[0] == create_async_engine_mock
    assert async_sessionmaker_mock.call_args.kwargs == {"expire_on_commit": False}


async def test_disconnect(mocker):
    """
    Tests the disconnect function for completion. The disconnect
    function should run without any errors

    :param mocker: Fixture to mock specific functions for testing
    """
    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_DB_TYPE = "native"
    mocker.patch.object(connection, "settings", settings_mock)

    # Mocks the db-connection class
    db_connection_mock = MagicMock(spec=DatabaseConnection)
    db_connection_mock._display_name = ""
    db_connection_mock._engine = MagicMock(spec_set=AsyncEngine)

    # Invokes the database-connection disconnect function
    await DatabaseConnection.disconnect(self=db_connection_mock)

    # Checks whether the required methods were called correctly
    assert db_connection_mock._engine.dispose.call_count == 1


async def test_disconnect_cloud(mocker):
    """
    Tests the disconnect function for completion. The disconnect
    function should run without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_DB_TYPE = "cloud"
    mocker.patch.object(connection, "settings", settings_mock)

    # Mocks the db-connection class
    db_connection_mock = MagicMock(spec=DatabaseConnection)
    db_connection_mock._connector = MagicMock(spec_set=Connector)
    db_connection_mock._display_name = "display-name"
    db_connection_mock._engine = MagicMock(spec_set=AsyncEngine)

    # Invokes the database-connection disconnect function
    await DatabaseConnection.disconnect(self=db_connection_mock)

    # Checks whether the required methods were called correctly
    assert db_connection_mock._connector.close_async.called
    assert db_connection_mock._engine.dispose.call_count == 1


async def test_get_cloud_sql_creator(mocker):
    """
    Tests the _get_cloud_sql_creator function for completion. The
    _get_cloud_sql_creator function should return a Cloud SQL creator
    without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_DB_CLOUD_INSTANCE = SecretStr("api-db-cloud-instance")
    settings_mock.API_DB_CLOUD_DRIVER = SecretStr("api-db-cloud-driver")
    settings_mock.API_DB_USER = SecretStr("api-db-user")
    settings_mock.API_DB_PASSWORD = SecretStr("api-db-password")
    settings_mock.API_DB_DB = SecretStr("api-db-db")
    settings_mock.API_DB_CLOUD_IS_PRIVATE = True
    mocker.patch.object(connection, "settings", settings_mock)

    # Mocks the connector class
    creator_mock = MagicMock()
    connector_mock = MagicMock(spec_set=Connector)
    connector_mock.connect_async.return_value = creator_mock

    # Mocks the db-connection class
    db_connection_mock = MagicMock(spec=DatabaseConnection)
    db_connection_mock._connector = connector_mock

    # Invokes the _get_cloud_sql_creator function
    creator = await DatabaseConnection._get_cloud_sql_creator(self=db_connection_mock)

    # Checks whether the Cloud SQL creator was retrieved correctly
    assert creator == creator_mock
    assert connector_mock.connect_async.called
    assert connector_mock.connect_async.call_args.kwargs == {
        "enable_iam_auth": True,
        "instance_connection_string": "api-db-cloud-instance",
        "driver": "api-db-cloud-driver",
        "user": "api-db-user",
        "db": "api-db-db",
        "ip_type": IPTypes.PRIVATE,
    }


async def test_get_cloud_sql_creator_public(mocker):
    """
    Tests the _get_cloud_sql_creator function when a public IP should be used.
    The _get_cloud_sql_creator function should return a Cloud SQL creator
    without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mock and overrides the settings class
    settings_mock = MagicMock(spec=Settings)
    settings_mock.API_DB_CLOUD_INSTANCE = SecretStr("api-db-cloud-instance")
    settings_mock.API_DB_CLOUD_DRIVER = SecretStr("api-db-cloud-driver")
    settings_mock.API_DB_USER = SecretStr("api-db-user")
    settings_mock.API_DB_PASSWORD = SecretStr("api-db-password")
    settings_mock.API_DB_DB = SecretStr("api-db-db")
    settings_mock.API_DB_CLOUD_IS_PRIVATE = False
    mocker.patch.object(connection, "settings", settings_mock)

    # Mocks the connector class
    creator_mock = MagicMock()
    connector_mock = MagicMock(spec_set=Connector)
    connector_mock.connect_async.return_value = creator_mock

    # Mocks the db-connection class
    db_connection_mock = MagicMock(spec=DatabaseConnection)
    db_connection_mock._connector = connector_mock

    # Invokes the _get_cloud_sql_creator function
    creator = await DatabaseConnection._get_cloud_sql_creator(self=db_connection_mock)

    # Checks whether the Cloud SQL creator was retrieved correctly
    assert creator == creator_mock
    assert connector_mock.connect_async.called
    assert connector_mock.connect_async.call_args.kwargs == {
        "enable_iam_auth": True,
        "instance_connection_string": "api-db-cloud-instance",
        "driver": "api-db-cloud-driver",
        "user": "api-db-user",
        "db": "api-db-db",
        "ip_type": IPTypes.PUBLIC,
    }
