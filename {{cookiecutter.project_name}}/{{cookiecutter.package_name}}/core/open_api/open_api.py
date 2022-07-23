from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from {{cookiecutter.package_name}}.core.settings import settings


def get_open_api_instance(app: FastAPI):
    """
    Function that gets the open api instance
    for the swagger documentation

    :param app: The FastAPI app instance

    :return: The open api schema
    """

    # Returns the existing open api schema
    if app.openapi_schema:
        return app.openapi_schema

    # Creates the open api schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        routes=app.routes,
    )

    # Returns the open api schema
    app.openapi_schema = openapi_schema
    return app.openapi_schema
