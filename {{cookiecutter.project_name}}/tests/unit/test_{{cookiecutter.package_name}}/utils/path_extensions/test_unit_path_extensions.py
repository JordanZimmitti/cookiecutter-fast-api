from {{cookiecutter.package_name}}.utils.modules.path_extensions import get_parent_path_by_file


def test_get_parent_path_by_file_exists():
    """
    Tests the get_parent_path_by_file function when a parent path is found.
    The get_parent_path_by_file function should return a parent path
    """

    # Checks whether the parent path was retrieved correctly
    parent_path = get_parent_path_by_file("pyproject.toml")
    assert str(parent_path)


def test_get_parent_path_by_file_not_exists():
    """
    Tests the get_parent_path_by_file function when a parent path is not found.
    The get_parent_path_by_file function should return None
    """

    # Checks whether None is retrieved
    parent_path = get_parent_path_by_file("file_does_not_exist.py")
    assert "None" in str(parent_path)
