from contextlib import asynccontextmanager

from fastapi import FastAPI

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.services.logger import start_logger

from .app import deconstruct_app_state, setup_app_state


class ApiLifeSpan:
    def __init__(self):
        """
        Class that handles the lifecycle
        of the FastAPI server
        """
        
        # Creates the given fields
        self._app: FastAPI | None = None

    @asynccontextmanager
    async def begin(self, app: FastAPI):
        """
        Function that begins monitoring the
        lifecycle of the FastAPI server

        :param app: The FastAPI app instance
        """

        # Sets the FastAPI app instance
        self._app = app

        # Executes the lifespan functions
        await self._on_api_startup()
        await self._repeated_tasks()
        yield
        await self._on_api_shutdown()

    async def _on_api_startup(self):
        """
        Function that runs before the FastAPI
        server begins taking requests
        """

        # Starts the logger and gets its instance
        start_logger(settings.LOG_LEVEL)

        # Configures the fast-api state instances
        setup_app_state(self._app)

    async def _on_api_shutdown(self):
        """
        Function that runs before the FastAPI
        server stops taking requests
        """

        # Deconstructs the fast-api state instances
        await deconstruct_app_state(self._app)

    async def _repeated_tasks(self):
        """
        Function that starts all background repeated
        tasks that run on a scheduled interval
        """
        pass