from unittest.mock import MagicMock

from fastapi import Request

from {{cookiecutter.package_name}}.api.dependencies.database import get_db_manager
from {{cookiecutter.package_name}}.core.database import DatabaseManager


def test_get_db_manager():
    """
    Tests the get_db_manager function for completion. The get_db_manager function
    should return a database manager instance with a test database display name
    """

    # Mocks the request and db-manager classes
    request_mock = MagicMock(spec_set=Request)
    db_manager_mock = MagicMock(spec_set=DatabaseManager)

    # Adds a test database friendly name to the db-manager mock
    db_manager_mock.display_name = "Test Database Name"

    # Adds the db-manager mock to the request mock
    request_mock.app.state.db_manager = db_manager_mock

    # Checks whether the db-manager mock is retrieved correctly
    db_manager = get_db_manager(request_mock)
    assert db_manager.display_name == "Test Database Name"
