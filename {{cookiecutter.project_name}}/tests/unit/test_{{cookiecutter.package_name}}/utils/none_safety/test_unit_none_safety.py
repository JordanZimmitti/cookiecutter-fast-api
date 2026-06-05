from pytest import raises

from {{cookiecutter.package_name}}.utils.none_safety import ns


def test_none_safety():
    """
    Tests the none_safety function when a value exists. The none_safety
    function should return the value without any errors
    """

    # Invokes the none_safety function
    value = ns(value="test")

    # Checks whether the correct value was retrieved
    assert value == "test"


def test_none_safety_default():
    """
    Tests the none_safety function when a value is None, but a default value
    is provided. The none_safety function should return the default value
    without any errors
    """

    # Invokes the none_safety function
    value = ns(value=None, default="test")

    # Checks whether the correct value was retrieved
    assert value == "test"


def test_none_safety_none():
    """
    Tests the none_safety function when a value is None. The
    none_safety function should raise a ValueError
    """

    # Checks whether the correct error was raised
    with raises(ValueError):
        ns(value=None)
