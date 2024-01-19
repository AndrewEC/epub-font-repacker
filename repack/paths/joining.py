from pathlib import Path

from repack.opf import find_path_to_opf_file

def get_relative_joining_path(temp_path: Path, child_path: Path) -> str:
    """
    Attempts to determine the number of parent directories that sit between the child_path and the temp_path.

    For example if we have a temp_path of C:\\testing\\temp and a child_path of C:\\testing\\temp\\content\\chapters
    this function will return ../../ indicating that there are two parent directories that must be traversed in order
    to go from the child_path to the temp_path.

    :param temp_path: The absolute path to the location where the contents of the input epub file were extracted to.
    :param child_path: The path from which we will determine the number of parent directories that need to be
        traversed before we reach the temp_path
    :return: A string representing the number of parent directories that need to be traversed to get from the
        child_path to the temp_path.
    :raises ValueError: Raised if there is no common ancestry between the temp_path and the child_path. This
        shouldn't reasonably occur unless the temp_path and child_path are on two separate drives.
    """
    next_path = child_path if child_path.is_dir() else child_path.parent
    if temp_path.name == next_path.name:
        return ''
    parent_folder_count = 0
    while temp_path.name != next_path.name:
        # If next_path and the next_path parent are equal then next_path has no parent meaning we have
        # reached the root of the drive and there is no common ancestry between the two paths.
        if next_path == next_path.parent:
            raise ValueError(f'There is no common parent directory between: [{temp_path}] and [{child_path}]')
        next_path = next_path.parent
        parent_folder_count = parent_folder_count + 1
    return '../' * parent_folder_count


def get_relative_joining_path_to_manifest(temp_path: Path) -> str:
    """
    Attempts to determine the relative joining path between the temp_path and the manifest file (OPF file).

    See get_relative_joining_path for details on how the relative joining path is determined.

    :param temp_path: The absolute path to the temp folder in which the contents of the input file have been extracted
        to.
    :return: A string representing the number of parent directories that need to be traversed to get from the
        OPF tile to the temp_path.
    """
    opf_file_path = find_path_to_opf_file(temp_path)
    return get_relative_joining_path(temp_path, opf_file_path)
