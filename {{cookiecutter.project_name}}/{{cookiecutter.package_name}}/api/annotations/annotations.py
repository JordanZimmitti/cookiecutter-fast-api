from typing import Annotated, Tuple

from fastapi import Depends

from {{cookiecutter.package_name}}.api.dependencies.cache import get_redis_manager
from {{cookiecutter.package_name}}.api.dependencies.database import get_db_manager
from {{cookiecutter.package_name}}.api.dependencies.middleware import get_request_metadata
from {{cookiecutter.package_name}}.core.cache import RedisManager
from {{cookiecutter.package_name}}.core.database import DatabaseManager

# Annotates all dependencies used in routes
DepDatabaseManager = Annotated[DatabaseManager, Depends(get_db_manager)]
DepRedisManager = Annotated[RedisManager, Depends(get_redis_manager)]
DepRequestMetadata = Annotated[Tuple[str, str, str], Depends(get_request_metadata)]
