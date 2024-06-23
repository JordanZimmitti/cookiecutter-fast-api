from abc import ABC
from logging import getLogger
from typing import Any, Dict

from fastapi import FastAPI
from gunicorn.app.base import BaseApplication
from starlette.responses import JSONResponse
from uvicorn.workers import UvicornWorker

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.exceptions import (
    BadRequestError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthenticatedError,
    ValidationError,
)

from .app import setup_app
from .lifespan import ApiLifeSpan

# Gets the {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.app.{{cookiecutter.package_name}}_base")


class {{cookiecutter.class_name}}UvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop": settings.UVICORN_LOOP,
        "http": settings.UVICORN_HTTP,
        "interface": settings.UVICORN_INTERFACE,
        "headers": [("server", settings.PROJECT_NAME)],
    }


class {{cookiecutter.class_name}}Base(BaseApplication, ABC):

    # Creates the fast-api instance
    _app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=settings.DOCS_URL,
        debug=settings.IS_FAST_API_DEBUG,
        lifespan=ApiLifeSpan().begin,
    )

    def __init__(self, options: Dict[str, Any] | None):
        """
        Class that configures standing up the {{cookiecutter.friendly_name}}
        server using gunicorn

        :param options: The gunicorn/uvicorn server configuration options
        """

        # Setup fast-api app instance
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
        message = f"Bad Request Error: {exc.detail}"
        logger.error(message)
        return JSONResponse(status_code=exc.status_code, content={"message": message})

    @staticmethod
    @_app.exception_handler(ForbiddenError)
    async def forbidden_error_handler(_, exc: ForbiddenError) -> JSONResponse:

        # Sends the forbidden-error response
        message = f"Forbidden Error: {exc.detail}"
        logger.error(message)
        return JSONResponse(status_code=exc.status_code, content={"message": message})

    @staticmethod
    @_app.exception_handler(InternalServerError)
    async def internal_server_error_handler(_, exc: InternalServerError) -> JSONResponse:

        # Sends the internal-server-error response
        message = f"Internal Server Error: {exc.detail}"
        logger.error(message)
        return JSONResponse(status_code=exc.status_code, content={"message": message})

    @staticmethod
    @_app.exception_handler(NotFoundError)
    async def not_found_error_handler(_, exc: NotFoundError) -> JSONResponse:

        # Sends the not-found-error response
        message = f"Not Found Error: {exc.detail}"
        logger.error(message)
        return JSONResponse(status_code=exc.status_code, content={"message": message})

    @staticmethod
    @_app.exception_handler(UnauthenticatedError)
    async def unauthenticated_error_handler(_, exc: UnauthenticatedError) -> JSONResponse:

        # Sends the unauthenticated-error response
        message = f"Unauthenticated Error: {exc.detail}"
        logger.error(message)
        return JSONResponse(status_code=exc.status_code, content={"message": message})

    @staticmethod
    @_app.exception_handler(ValidationError)
    async def validation_error_handler(_, exc: ValidationError) -> JSONResponse:

        # Sends the validation-error response
        message = f"Validation Error: {exc.detail}"
        logger.error(message)
        return JSONResponse(status_code=exc.status_code, content={"message": message})
