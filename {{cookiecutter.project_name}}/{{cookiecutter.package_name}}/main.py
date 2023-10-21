from abc import ABC
from logging import getLogger
from typing import Any, Callable, Dict

from fastapi import status
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response

from {{cookiecutter.package_name}}.core.app import {{cookiecutter.class_name}}Base, handle_request
from {{cookiecutter.package_name}}.core.settings import settings

# Gets the {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.main")


class {{cookiecutter.class_name}}({{cookiecutter.class_name}}Base, ABC):

    # Gets the fast-api instance from the base class
    app = {{cookiecutter.class_name}}Base._app

    def __init__(self, options: Dict[str, Any] | None):
        super().__init__(options)

    @staticmethod
    @app.middleware("http")
    async def handle_request_middleware(request: Request, call_next: Callable) -> Response:
        """
        Function that handles the incoming request
        and send the response back to the client

        :param request: The incoming http request sent from a client
        :param call_next: The endpoint to call next to get the appropriate response

        :return: The response to the client
        """
        try:
            return await handle_request({{cookiecutter.class_name}}.app, request, call_next)
        except Exception as exc:
            message = "Internal Server Error: An unexpected error occurred, please try again"
            logger.critical(message)
            logger.debug(message, exc_info=exc)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": message}
            )

    @staticmethod
    @app.get("/", include_in_schema=False)
    @app.get("/api", include_in_schema=False)
    @app.get(settings.API_PREFIX, include_in_schema=False)
    async def redirect_to_docs():
        """
        Base route that redirects to the {{cookiecutter.friendly_name}} server
        open-api swagger documentation
        """
        response = RedirectResponse(url=settings.DOCS_URL)
        return response


if __name__ == "__main__":
    {{cookiecutter.class_name}}(
        options={
            "bind": f"0.0.0.0:{settings.LISTEN_PORT}",
            "workers": settings.UVICORN_CONCURRENCY,
            "worker_class": "{{cookiecutter.package_name}}.core.app.{{cookiecutter.class_name}}UvicornWorker",
            "worker_connections": settings.UVICORN_CONNECTIONS,
            "max_requests": settings.UVICORN_MAX_REQUESTS,
            "max_requests_jitter": settings.UVICORN_MAX_REQUESTS_JITTER,
            "keepalive": settings.UVICORN_KEEP_ALIVE,
            "graceful_timeout": settings.UVICORN_GRACEFUL_TIMEOUT,
            "timeout": settings.UVICORN_TIMEOUT,
        }
    ).run()
