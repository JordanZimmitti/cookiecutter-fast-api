from typing import TypeVar

# Template return type
ReturnType = TypeVar("ReturnType")


def ns(value: ReturnType | None, default: ReturnType | None = None) -> ReturnType:
    """
    Utility function that checks for None safety. It takes a value that can be
    of any type or None, and returns the value if it is not None. If the value
    is None, it returns a default value if provided, or raises a ValueError if
    no default is given

    :param value: The value to check for None safety
    :param default: The default value to return if no value is provided

    :return: The value if safe, else default
    """

    # When the value and default are None, raises a ValueError
    if value is None and default is None:
        raise ValueError("Value cannot be None")

    # When the value is None, but a default is provided, return the default value
    if value is None and default is not None:
        return default

    # Returns the not None value
    return value
