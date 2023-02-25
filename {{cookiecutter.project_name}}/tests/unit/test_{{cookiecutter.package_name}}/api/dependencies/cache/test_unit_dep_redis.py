from unittest.mock import MagicMock

from {{cookiecutter.package_name}}.api.dependencies.cache import get_redis_manager
from {{cookiecutter.package_name}}.core.cache import RedisManager


def test_get_redis_manager():
    """
    Tests the get_redis_manager function for completion. The get_redis_manager
    function should return a RedisManager class instance without any errors
    """

    # Mocks the redis-manager class
    redis_manager_mock = MagicMock(spec_set=RedisManager)

    # Mocks the request class
    request_mock = MagicMock()
    request_mock.app.state.redis_manager = redis_manager_mock

    # Invokes the get_redis_manager function
    redis_manager = get_redis_manager(request_mock)

    # Checks whether the redis-manager was retrieved correctly
    assert redis_manager == redis_manager_mock
