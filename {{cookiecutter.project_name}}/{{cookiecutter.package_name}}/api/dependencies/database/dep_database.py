from fastapi import Request

from {{cookiecutter.package_name}}.core.database import DatabaseManager


def get_db_manager(request: Request) -> DatabaseManager:
    """
    Dependency function that gets the
    database manager instance

    :param request: The incoming FastAPI http request

    :return: The database manager instance
    """

    # Returns the database manager instance
    return request.app.state.db_manager
