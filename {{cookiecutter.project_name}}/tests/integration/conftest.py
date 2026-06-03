from os import environ

from pytest import Config, Parser, fixture

from tests.integration.client import ApiClient
from tests.integration.pytest_config_pro import PytestConfigPro


def pytest_addoption(parser: Parser):
    """
    Function that adds the valid arguments that can be
    used by the cli when running integration tests

    :param parser: The pytest parser
    """

    # Adds the cli argument options
    parser.addoption("--api_url", action="store")
    parser.addoption("--user_id", action="store")
    parser.addoption("--api_key", action="store")


@fixture(scope="session")
def client(pytestconfig: Config):
    """
    Pytest fixture that creates the client for
    hitting deployed API endpoints

    :param pytestconfig: Config to get the client parameters from the cli options when available

    :return: The API client
    """

    # Gets the cli arguments
    pytest_config = PytestConfigPro(pytestconfig)
    api_url = pytest_config.get_cli_argument("api_url", "http://127.0.0.1:2000/api")
    user_id = pytest_config.get_cli_argument("user_id", environ.get("USER_ID"))
    api_key = pytest_config.get_cli_argument("api_key", environ.get("API_KEY"))

    # Returns the API client instance
    api_client = ApiClient(api_url, None, user_id, api_key)
    if user_id and api_key:
        api_client.login()
    return api_client
