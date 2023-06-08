from asyncio import sleep

from {{cookiecutter.package_name}}.core.app import repeated_task


async def test_repeated_task():
    """
    Tests the repeated_task decorator function for completion. The repeated_task
    decorator function should repeat twice then stop without any errors
    """

    # The number of times the repeat function was repeated
    times_repeated = 0

    # Creates the decorated function that should be repeated 2 time every.5 seconds
    @repeated_task(period_seconds=0.01, repeat=2)
    async def repeat_function():
        nonlocal times_repeated
        times_repeated = times_repeated + 1
        if times_repeated == 2:
            empty_list = []
            _ = empty_list[0]

    # Invokes the decorated function
    await repeat_function()
    await sleep(0.2)

    # Checks whether the decorated function was repeated the correct number of times
    assert times_repeated == 3
