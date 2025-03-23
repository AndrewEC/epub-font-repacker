from pathlib import Path
from bs4 import BeautifulSoup
from functools import lru_cache

from repack.errors import (
    OpfException,
    ParseException,
    MissingContainerFileException,
    MissingOpfException
)
from repack.util import read_and_unlink


_OPF_FILE_EXTENSION = '.opf'
_MANIFEST_END_TAG = '</manifest>'
_CONTAINER_XML_LOCATION = 'META-INF/container.xml'
_OPF_MEDIA_TYPE = 'application/oebps-package+xml'
_MEDIA_TYPE_PROPERTY = 'media-type'
_FULL_PATH_PROPERTY = 'full-path'


def _read_container_file(temp_path: Path) -> str:
    container_path = temp_path.joinpath(_CONTAINER_XML_LOCATION)
    if not container_path.is_file():
        raise MissingContainerFileException(container_path)
    with open(container_path, 'r', encoding='utf-8') as container_file:
        return ''.join(container_file.readlines())


def _find_relative_opf_file_location(container_content: str) -> str:
    try:
        root_file_list = BeautifulSoup(container_content, features='xml').find('container').find('rootfiles').find_all('rootfile')
        opf_location_node = next((root_file for root_file in root_file_list if root_file[_MEDIA_TYPE_PROPERTY] == _OPF_MEDIA_TYPE), None)
        return opf_location_node[_FULL_PATH_PROPERTY]
    except Exception as e:
        raise ParseException(e) from e


@lru_cache()
def find_path_to_opf_file(temp_path: Path) -> Path:
    """
    Retrieve the absolute path to the OPF file (sometimes referred to the manifest file).

    This searches for the location of the opf file by reading in the standard container.xml file, looking for the list
    of files specified within the container->rootfiles->rootfile node, and searching for a file defined with a
    media-type of application/oebps-package+xml.

    :param temp_path: The path to the temp folder in which the contents of the input epub file were extracted to.
    :return: A Path object containing the absolute path to the OPF file.
    :raises OpfLocationException: Raised if the OPF file cannot be found.
    """
    try:
        container_content = _read_container_file(temp_path)
        relative_opf_location = _find_relative_opf_file_location(container_content)
        opf_path = temp_path.joinpath(relative_opf_location).absolute()
        if not opf_path.is_file():
            raise MissingOpfException(opf_path)
        return opf_path
    except Exception as e:
        raise OpfException(e) from e


def add_manifest_entry_to_opf_file(temp_path: Path, opf_manifest_item: str):
    """
    Finds the location of the OPF file extracted from the input epub file and inserts the specified manifest entry at
    the end of the manifest just before the closing </manifest> tag.

    :param temp_path: The path to the temp folder in which the contents of the input epub file were extracted to.
    :param opf_manifest_item: The fully formed XML manifest entry node to add to the OPF file.
    :raises OpfLocationException: Raised if the OPF file cannot be found.
    """
    opf_file_path = find_path_to_opf_file(temp_path)
    current_lines = read_and_unlink(opf_file_path)
    with open(opf_file_path, 'w', encoding='utf-8') as file:
        for line in current_lines:
            if _MANIFEST_END_TAG in line:
                file.write(opf_manifest_item)
            file.write(line)
