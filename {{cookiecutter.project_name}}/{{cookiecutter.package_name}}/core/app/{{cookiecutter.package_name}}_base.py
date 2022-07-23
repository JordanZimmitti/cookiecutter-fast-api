from abc import ABC
from typing import Any, Dict

from fastapi import FastAPI
from gunicorn.app.base import BaseApplication
from starlette.responses import JSONResponse

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.exceptions import (
    BadRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthenticatedError,
)

from .app import setup_app


class {{cookiecutter.class_name}}Base(BaseApplication, ABC):

    # Creates the fast-api instance
    _app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=settings.DOCS_URL,
        debug=settings.IS_FAST_API_DEBUG,
    )

    def __init__(self, options: Dict[str, Any] | None):
        """
        Class that configures standing up the {{cookiecutter.friendly_name}}
        server using gunicorn

        :param options: The gunicorn/uvicorn server configuration options
        """

        # Setup FastAPI app instance
        setup_app(self._app)

        # Sets the class variables and instantiates the BaseApplication
        self._options = options or {}
        super().__init__()

    def load_config(self):
        """
        Function that builds the gunicorn
        server configuration
        """

        # Gets the gunicorn server configuration
        config = {
            key: value
            for key, value in self._options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """
        Function that starts the
        fast-api application
        """
        return self._app

    @staticmethod
    @_app.exception_handler(BadRequestError)
    async def bad_request_error_handler(_, exc: BadRequestError) -> JSONResponse:

        # Sends the bad-request-error response
        content = {"message": f"Bad Request Error: {exc.detail}"}
        return JSONResponse(status_code=exc.status_code, content=content)

    @staticmethod
    @_app.exception_handler(ForbiddenError)
    async def forbidden_error_handler(_, exc: ForbiddenError) -> JSONResponse:

        # Sends the forbidden-error response
        content = {"message": f"Forbidden Error: {exc.detail}"}
        return JSONResponse(status_code=exc.status_code, content=content)

    @staticmethod
    @_app.exception_handler(InternalServerError)
    async def internal_server_error_handler(_, exc: InternalServerError) -> JSONResponse:

        # Sends the internal-server-error response
        content = {"message": f"Internal Server Error: {exc.detail}"}
        return JSONResponse(status_code=exc.status_code, content=content)

    @staticmethod
    @_app.exception_handler(NotFoundError)
    async def not_found_error_handler(_, exc: NotFoundError) -> JSONResponse:

        # Sends the not-found-error response
        content = {"message": f"Not Found Error: {exc.detail}"}
        return JSONResponse(status_code=exc.status_code, content=content)

    @staticmethod
    @_app.exception_handler(UnauthenticatedError)
    async def unauthenticated_error_handler(_, exc: UnauthenticatedError) -> JSONResponse:

        # Sends the unauthenticated-error response
        content = {"message": f"Unauthenticated Error: {exc.detail}"}
        return JSONResponse(status_code=exc.status_code, content=content)
