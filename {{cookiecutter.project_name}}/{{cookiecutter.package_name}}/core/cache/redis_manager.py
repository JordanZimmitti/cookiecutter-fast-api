from logging import getLogger
from typing import Any, Callable

from pydantic import SecretStr
from redis.asyncio.client import Redis
from redis.client import Pipeline
from tenacity import retry, stop_after_attempt, wait_fixed

from {{cookiecutter.package_name}}.core.settings import settings
from {{cookiecutter.package_name}}.exceptions import InternalServerError

# Gets {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.cache.redis_manager")


class RedisManager:
    def __init__(
        self,
        display_name: str,
        description: str,
        host: SecretStr,
        port: SecretStr,
        password: SecretStr,
    ):
        """
        Class that handles various
        redis operations

        :param display_name: The name of the redis instance to display to the client
        :param description: The description of the redis instance
        :param host: The host of the redis instance
        :param port: The port of the redis instance
        :param password: The password of the redis instance
        """

        # Initializes given variables
        self._display_name = display_name
        self._description = description
        self._host = host
        self._port = port
        self._password = password

        # Initializes class-created variables
        self._operation: Redis | None = None

    @property
    def display_name(self) -> str:
        """
        Property that gets the name of the redis
        instance to display to the client

        :return: The redis instance display name
        """
        return self._display_name

    @property
    def description(self) -> str:
        """
        Property that gets the description
        of the redis instance

        :return: The redis instance description
        """
        return self._description

    @property
    def operation(self) -> Redis:
        """
        Property that gets the redis instance
        for performing redis operations

        :return: The redis instance
        """

        # Checks whether the async redis instance exists
        if self._operation is None:
            logger.info("The redis instance is not connected, was the connect function called?")
            raise InternalServerError()

        # Returns the redis instance
        return self._operation

    def connect(self):
        """
        Function that creates the async redis instance
        connection for handing redis operations
        """

        # Initializes the redis instance for performing operations
        self._operation = Redis(
            host=self._host.get_secret_value(),
            port=int(self._port.get_secret_value()),
            password=self._password.get_secret_value(),
            decode_responses=settings.API_REDIS_DECODE_RESPONSES,
        )

        # Logs that the provided redis instance has been connected successfully
        logger.info(f"Connected to the {self._display_name} instance")

    async def disconnect(self):
        """
        Function that disconnects the
        async redis instance
        """

        # Disconnects the async redis instance
        await self._operation.close()
        logger.info(f"Disconnected the {self._display_name} instance")

    @retry(stop=stop_after_attempt(settings.API_REDIS_PIPELINE_RETRY_NUMBER), wait=wait_fixed(1))
    async def pipeline(
        self,
        pipe_ops: Callable[[Pipeline], None],
        is_transaction: bool = True,
        is_scalar: bool = False,
    ) -> Any:
        """
        Function that wraps the redis pipeline function in a try/catch to handle unexpected errors.
        The redis pipeline function queues multiple commands for later execution. Apart from making
        a group of operations atomic, pipelines are useful for reducing the back-and-forth overhead
        between the client and server

        :param pipe_ops: A function that contains redis operations to add to the pipeline
        :param is_transaction: Whether all commands should be executed atomically
        :param is_scalar: Whether the result returned is a scalar
        """

        # Attempts to execute redis-operations in the pipeline
        try:
            async with self._operation.pipeline(is_transaction) as pipe:
                pipe_ops(pipe)
                result = await pipe.execute()
                return result[0] if is_scalar else result
        except Exception as exc:
            message = "Redis pipeline execute failed"
            logger.error(message)
            logger.debug(message, exc_info=exc)
            raise InternalServerError()
