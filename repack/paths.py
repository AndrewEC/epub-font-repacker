from pathlib import Path
import uuid

from repack.opf import find_path_to_opf_file


_RESOURCE_FOLDER = 'resources'
_DESTINATION_RESOURCE_NAME_TEMPLATE = 'resource{}{}'


def get_path_to_resource(resource_name: str) -> Path:
    """
    Retrieves the absolute path to a file located within the resources folder located in the same directory as
    this source file.

    This does not perform any check to ensure the file in question exists.

    :param resource_name: The name of the file within the resources folder that we need the absolute path of.
    :return: The absolute path to the resources in the resources folder.
    """
    return Path(__file__).absolute().parent.joinpath(_RESOURCE_FOLDER).joinpath(resource_name)


def generate_destination_file_name(source_file: Path) -> str:
    """
    Generates a random filename to act as a destination file name. The name will effectively be a randomly generated
    uuid, with the hyphens (-) removed, with the suffix, extension, pulled from the source_file appended onto it.

    :param source_file: The original name of the file from which the suffix of the file will be pulled as used as the
    suffix in the resulting generated name.
    :return: The name of the destination file. This filename will have the suffix, extension, that the input
    source_file has.
    """
    formatted_uuid = str(uuid.uuid4()).replace('-', '')
    return _DESTINATION_RESOURCE_NAME_TEMPLATE.format(formatted_uuid, source_file.suffix)


def get_relative_joining_path(temp_path: Path, child_path: Path) -> str:
    """
    Attempts to determine the number of parent directories that sit between the child_path and the temp_path.

    For example if we have a temp_path of C:\testing\temp and a child_path of C:\testing\temp\content\chapters
    this function will return ../../ indicating that there are two parent directories that must be traversed in order
    to go from the child_path to the temp_path.

    :param temp_path: The absolute path to the location where the contents of the input epub file were extracted to.
    :param child_path: The path from which we will determine the number of parent directories that need to be
    traversed before we reach the temp_path
    :return: A string representing the number of parent directories that need to be traversed to get from the
    child_path to the temp_path.
    :raises Exception: Raised if the temp path is not a direct or related parent of the child_path.
    """
    next_path = child_path if child_path.is_dir() else child_path.parent
    if temp_path.name == next_path.name:
        return ''
    parent_folder_count = 0
    while temp_path.name != next_path.name:
        if next_path == next_path.parent:
            raise Exception(f'There is no common parent directory between: [{temp_path}] and [{child_path}]')
        next_path = next_path.parent
        parent_folder_count = parent_folder_count + 1
    return '../' * parent_folder_count


def get_relative_joining_path_to_manifest(temp_path: Path) -> str:
    """
    Attempts to determine the relative joining path between the temp_path the manifest, OPF, file.

    See get_relative_joining_path for details on how the relative joining path is determined.

    :param temp_path: The absolute path to the temp folder in which the contents of the input file have been extracted
    to.
    :return: A string representing the number of parent directories that need to be traversed to get from the
    OPF tile to the temp_path.
    """
    opf_file_path = find_path_to_opf_file(temp_path)
    return get_relative_joining_path(temp_path, opf_file_path)
