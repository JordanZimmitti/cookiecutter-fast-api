from asyncio import AbstractEventLoop, get_event_loop_policy
from os import listdir, remove
from os.path import dirname, exists, join, pardir
from typing import Any, Generator

from dotenv import load_dotenv
from pytest_asyncio import fixture

# Loads environment variables
parent_directory = join(dirname(__file__), pardir)
pytest_env_directory = join(parent_directory, "pytest.env")
load_dotenv(pytest_env_directory)


@fixture(scope="session", autouse=True)
def cleanup() -> Generator[None, Any, None]:
    """
    Pytest fixture that cleans up generated files
    and folders created during testing
    """

    # Yield nothing, waits for testing to finish
    yield None

    # Import packages after pytest environment variables are loaded
    from {{cookiecutter.package_name}}.core.settings import settings
    from {{cookiecutter.package_name}}.utils.modules.path_extensions import get_parent_path_by_file

    # Removes the application log file
    project_path = f"{get_parent_path_by_file('pyproject.toml')}"
    log_directory = f"{project_path}/{settings.LOG_FILE_DIRECTORY}/"
    if exists(log_directory):
        for file in listdir(log_directory):
            remove(join(log_directory, file))


@fixture(scope="session", autouse=True)
def event_loop() -> Generator[AbstractEventLoop, Any, None]:
    """
    Pytest fixture that creates an event-loop
    for asynchronous operations

    :return: The new event loop
    """

    # Returns the newly started event-loop
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
