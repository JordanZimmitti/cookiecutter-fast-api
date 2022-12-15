from unittest.mock import MagicMock

from pydantic import SecretStr
from sqlalchemy.orm import sessionmaker

from {{cookiecutter.package_name}}.core.database import manager
from {{cookiecutter.package_name}}.core.database.connection import DatabaseConnection
from {{cookiecutter.package_name}}.core.database.manager import DatabaseManager
from {{cookiecutter.package_name}}.core.database.row_operations import DatabaseRowOperations


def test_get_connection():
    """
    Tests the connection property for completion. The connection property
    should return a DatabaseConnection class instance without any errors
    """

    # Mocks the database-connection class
    database_connection_mock = MagicMock(spec_set=DatabaseConnection)

    # Creates the db_manager instance
    db_manager = DatabaseManager(
        display_name="test-display-name",
        description="test-description",
        db_uri=SecretStr("test-db-uri"),
    )
    db_manager._connection = database_connection_mock

    # Checks whether the mocked database-connection class was retrieved correctly
    db_connection = db_manager.connection
    assert db_connection == database_connection_mock


def test_get_description():
    """
    Tests the description property for completion. The
    description property should return a description
    """

    # Creates the db_manager instance
    db_manager = DatabaseManager(
        display_name="test-name", description="test-description", db_uri=SecretStr("test-db-uri")
    )

    # Checks whether the description was retrieved correctly
    description = db_manager.description
    assert description == "test-description"


def test_get_display_name():
    """
    Tests the display_name property for completion. The
    display_name property should return a display_name
    """

    # Creates the db-manager instance
    db_manager = DatabaseManager(
        display_name="test-name", description="test-description", db_uri=SecretStr("test-db-uri")
    )

    # Checks whether the display-name was retrieved correctly
    display_name = db_manager.display_name
    assert display_name == "test-name"


def test_get_row_operations(mocker):
    """
    Tests the row_operations property for completion. The row_operations property
    should return a DatabaseRowOperations class instance without any errors

    :param mocker: Fixture to mock specific functions for testing
    """

    # Mocks the database-connection class
    database_connection_mock = MagicMock(spec_set=DatabaseConnection)
    database_connection_mock.session_maker = MagicMock(spec_set=sessionmaker)

    # Mocks and overrides the database-row-operations class
    database_row_operations_mock = MagicMock(spec_set=DatabaseRowOperations)
    mocker.patch.object(manager, "DatabaseRowOperations", return_value=database_row_operations_mock)

    # Creates the db_manager instance
    db_manager = DatabaseManager(
        display_name="test-display-name",
        description="test-description",
        db_uri=SecretStr("test-db-uri"),
    )
    db_manager._connection = database_connection_mock

    # Checks whether the mocked database-row-operations class was retrieved correctly
    db_row_operations = db_manager.row_operations
    assert db_row_operations == database_row_operations_mock


def test_init():
    """
    Tests the DatabaseManager init function for completion. The DatabaseManager init
    function should instantiate a DatabaseManager instance without any errors
    """

    # Define and instantiates the database-manager class
    db_manager = DatabaseManager(
        display_name="test-display-name",
        description="test-description",
        db_uri=SecretStr("test-db-uri"),
    )

    # Checks whether the database-manager class correctly instantiated
    assert db_manager._display_name == "test-display-name"
    assert db_manager._description == "test-description"
    assert db_manager._db_uri == SecretStr("test-db-uri")
