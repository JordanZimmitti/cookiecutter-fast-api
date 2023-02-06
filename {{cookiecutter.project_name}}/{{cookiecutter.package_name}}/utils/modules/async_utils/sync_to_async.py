from asyncio import get_running_loop
from typing import Callable


async def run_sync_function(sync_function: Callable, *args):
    """
    Function that runs a synchronous
    function asynchronously

    :param sync_function: The synchronous function to run asynchronously
    :param args: The arguments needed by the synchronous function

    :return: The result of the synchronous function
    """

    # Runs the synchronous function in an asynchronous event loop
    loop = get_running_loop()
    return await loop.run_in_executor(None, sync_function, *args)
