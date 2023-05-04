from asyncio import ensure_future, sleep
from functools import update_wrapper
from logging import getLogger
from typing import Callable

# Gets the {{cookiecutter.friendly_name}} server logger instance
logger = getLogger("{{cookiecutter.package_name}}.core.app.repeat")


def repeated_task(period_seconds: float, repeat: int = 0):
    """
    Decorator function that invokes the attached function repeatedly after a period of seconds has
    passed. When repeat is set to zero (default), the repeated task will be invoked indefinitely.
    When the attached function throws an exception it will not count as a repeat attempt

    :param period_seconds: The number of seconds to wait before invoking the attached function
    :param repeat: Number of times to invoke the attached function
    """

    # Creates the decorator function
    def decorator(func: Callable):
        """
        Function getting the
        attached function

        :param func: The function attached to the decorator
        """

        # Creates the wrapper function
        async def wrapper():
            """
            Wrapper function that configures the attached function to
            invoke repeatedly after a period of seconds has passed
            """

            # Function for executes the repeated task concurrently
            async def execute_repeated_task():

                # Waits the given period before invoking the attached function periodically
                await sleep(period_seconds)
                repeated = 0
                while repeat == 0 or repeated < repeat:

                    # Executes the repeated task
                    try:
                        await func()
                        if repeat != 0:
                            repeated = repeated + 1
                        logger.debug("repeated task executed successfully")
                    except Exception as exc:
                        message = "The repeated task failed to run"
                        logger.critical(message)
                        logger.debug(message, exc_info=exc)

                    # Waits the given period before invoking the attached function again
                    await sleep(period_seconds)

            # Schedules the repeated task to run concurrently with other tasks
            ensure_future(execute_repeated_task())

        # Updates the wrapper function
        return update_wrapper(wrapper, func)

    # Returns the decorator
    return decorator
