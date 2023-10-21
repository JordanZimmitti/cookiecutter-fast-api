from logging import getLogger
from time import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from {{cookiecutter.package_name}}.api.dependencies.middleware import (
    get_request_metadata,
    get_response_size,
    set_correlation_id,
)
from {{cookiecutter.package_name}}.core.cache import FastApiContext, RedisManager, get_fast_api_context
from {{cookiecutter.package_name}}.core.database import DatabaseManager
from {{cookiecutter.package_name}}.core.open_api import get_open_api_instance
from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.services.logger import HealthCheckFilter

from .router import api_router

# Gets the {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.app.app.request")
logger.addFilter(HealthCheckFilter())


def setup_app(app: FastAPI):
    """
    Function that configures the FastAPI instance
    before app startup

    :param app: The FastAPI app instance
    """

    # Sets all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_headers=["*"],
            allow_methods=["*"],
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        )

    # Sets the main router instance
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # Sets the custom open-api instance
    app.openapi = lambda: get_open_api_instance(app)

    # Exposes the metrics endpoint
    expose_metrics_endpoint(app)


def expose_metrics_endpoint(app: FastAPI):
    """
    Function that exposes the Fast API metrics endpoint
    to see Prometheus metrics

    :param app: The FastAPI app instance
    """

    # Exposes the API metrics as an endpoint
    instrumentator = Instrumentator(excluded_handlers=[rf"{settings.API_PREFIX}/metrics"])
    instrumentator.instrument(app)
    instrumentator.expose(app, endpoint=f"{settings.API_PREFIX}/metrics", tags=["Metrics"])


def setup_app_state(app: FastAPI):
    """
    Function that configures the FastAPI
    state instances during startup

    :param app: The FastAPI app instance
    """

    # Adds the fast-api-context into the app state
    fast_api_context = get_fast_api_context()
    app.state.fast_api_context = fast_api_context

    # Adds the database manager instance into the app state when it is enabled
    if settings.IS_API_DB_ENABLED:
        db_manager = DatabaseManager(
            settings.API_DB_DISPLAY_NAME,
            settings.API_DB_DESCRIPTION,
            settings.API_DB_CONN_URI,
        )
        app.state.db_manager = db_manager

        # Connects to the database
        db_manager.connection.connect()

    # Adds the redis instance into the app state when it is enabled
    if settings.IS_API_REDIS_ENABLED:
        redis_manager = RedisManager(
            settings.API_REDIS_DISPLAY_NAME,
            settings.API_REDIS_DESCRIPTION,
            settings.API_REDIS_HOST,
            settings.API_REDIS_PORT,
            settings.API_REDIS_PASSWORD,
        )
        app.state.redis_manager = redis_manager

        # Connects to the redis instance
        redis_manager.connect()


async def deconstruct_app_state(app: FastAPI):
    """
    Function that deconstructs the FastAPI
    state instances during shutdown

    :param app: The FastAPI app instance
    """

    # Resets the context variables to their initial state
    fast_api_context: FastApiContext = app.state.fast_api_context
    fast_api_context.reset()

    # Disconnects the database connection pool when it is enabled
    if settings.IS_API_DB_ENABLED:
        db_manager: DatabaseManager = app.state.db_manager
        await db_manager.connection.disconnect()

    # Disconnects the redis instance when it is enabled
    if settings.IS_API_REDIS_ENABLED:
        redis_manager: RedisManager = app.state.redis_manager
        await redis_manager.disconnect()


async def handle_request(app: FastAPI, request: Request, call_next: Callable) -> Response:
    """
    Function that handles the incoming request
    and send the response back to the client

    :param app: The FastAPI app instance
    :param request: The request sent by the client
    :param call_next: The endpoint to call next to get the appropriate response

    :return: The response to the client
    """

    # Gets the fast-api-context instance from the FastAPI state
    fast_api_context: FastApiContext = app.state.fast_api_context

    # Gets the request metadata for logging
    request_metadata = get_request_metadata(request)

    # Sets the correlation-id for request log chaining
    set_correlation_id(request, fast_api_context)

    # Logs that the request has started
    start_extra = {
        "method": request_metadata.method,
        "url": request_metadata.url,
        "user_agent": request_metadata.user_agent
    }
    logger.info("Starting Request", extra=start_extra)

    # Handles the request and gets the response
    start_time = time()
    response: Response = await call_next(request)
    stop_time = time()

    # Gets the response metadata for logging
    status_code = response.status_code
    process_time = (stop_time - start_time) * 1000  # milliseconds

    # Logs that the request has finished
    finish_extra = {
        "method": request_metadata.method,
        "url": request_metadata.url,
        "status_code": status_code,
        "response_size_bytes": get_response_size(response),
        "response_time_ms": round(process_time, 3),
        "user_agent": request_metadata.user_agent,
    }
    logger.info("Finished Request", extra=finish_extra)

    # Returns the response
    fast_api_context.reset()
    return response
