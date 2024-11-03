from typing import List
from pathlib import Path


def read_and_unlink(file_path: Path) -> List[str]:
    """
    Reads in all the lines of the file in the specified path, deletes the file,
    then returns the read lines as a list.

    :param file_path: The path to the file to be read and deleted.
    :return: All the lines of the file as a string list.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    file_path.unlink(missing_ok=False)
    return lines
