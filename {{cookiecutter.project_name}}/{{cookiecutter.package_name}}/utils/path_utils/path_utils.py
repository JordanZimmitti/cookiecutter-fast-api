from os import getcwd
from os.path import isfile, join
from pathlib import Path


def get_parent_path_by_file(file_name: str, max_complexity: int = 10) -> Path | None:
    """
    Function that uses a file located within a parent directory to get the path of that parent
    directory. The get_parent_path_by_file function searches a set number of parent directories,
    once that number is reached and the file still does not exist 'none' will be returned

    :param file_name: The name of a file that is used to get the path of the directory it is in
    :param max_complexity: The amount of parent-directories to be searched before returning none

    :return:
        The path of the directory where the file is located, or none when the file can not be
        located
    """

    # Gets the current directory of this file
    current_directory = Path(getcwd())

    # Gets the path where the file-name exists
    for _ in range(0, max_complexity):

        # Creates the file path and checks whether it exists
        file_path = join(current_directory, file_name)
        if isfile(file_path):
            return current_directory

        # Gets the parent directory when the file path does not exist
        current_directory = current_directory.parent

    # When the max-complexity is reached and the file is still not found
    return None
