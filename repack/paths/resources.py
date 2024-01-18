from pathlib import Path
import uuid


_RESOURCE_FOLDER = 'resources'
_DESTINATION_RESOURCE_NAME_TEMPLATE = 'resource{}{}'
_TEMP_FOLDER_NAME_TEMPLATE = '_temp_{}'


def get_temp_path(epub_file: Path) -> Path:
    """
    Determines the temp path in which the contents of the epub file being processed can be extracted to so said
    contents can be further processed.

    :param epub_file: The path to the epub file being processed.
    :return: The absolute path to the temp directory.
    """
    return epub_file.parent.absolute().joinpath(_TEMP_FOLDER_NAME_TEMPLATE.format(epub_file.stem))


def get_path_to_resource(resource_name: str) -> Path:
    """
    Retrieves the absolute path to a file located within the resources folder located in the same directory as
    this source file.

    This does not perform any check to ensure the file in question exists.

    :param resource_name: The name of the file within the resources folder that we need the absolute path of.
    :return: The absolute path to the resources in the resources folder.
    """
    return Path(__file__).absolute().parent.parent.joinpath(_RESOURCE_FOLDER).joinpath(resource_name)


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
