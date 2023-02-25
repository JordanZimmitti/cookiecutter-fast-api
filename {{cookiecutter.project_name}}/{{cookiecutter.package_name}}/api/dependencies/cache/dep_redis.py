from fastapi import Request

from {{cookiecutter.package_name}}.core.cache import RedisManager


def get_redis_manager(request: Request) -> RedisManager:
    """
    Dependency function that gets the
    redis manager instance

    :param request: The incoming http request sent from a client

    :return: The redis manager instance
    """

    # Returns the redis manager instance
    return request.app.state.redis_manager
