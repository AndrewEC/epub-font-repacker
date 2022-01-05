from pathlib import Path
from bs4 import BeautifulSoup


_OPF_FILE_EXTENSION = '.opf'
_MANIFEST_END_TAG = '</manifest>'
_CONTAINER_XML_LOCATION = 'META-INF/container.xml'
_OPF_MEDIA_TYPE = 'application/oebps-package+xml'
_MEDIA_TYPE_PROPERTY = 'media-type'


class ParseException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


def _read_in_contents_of_container_file(temp_path: Path) -> str:
    container_path = temp_path.joinpath(_CONTAINER_XML_LOCATION)
    if not container_path.is_file():
        raise Exception(f'Could not find container.xml file at expected location: [{container_path}]')
    with open(container_path, 'r', encoding='utf-8') as container_file:
        return ''.join(container_file.readlines())


def _find_opf_location_in_container_content(container_content: str) -> str:
    try:
        root_file_list = BeautifulSoup(container_content, 'lxml').find('container').find('rootfiles').find_all('rootfile')
        location_node = next((root_file for root_file in root_file_list if root_file[_MEDIA_TYPE_PROPERTY] == _OPF_MEDIA_TYPE), None)
        if location_node is None:
            raise ParseException('Could not find location of OPF file in container.xml')
        return location_node['full-path']
    except Exception as e:
        if isinstance(e, ParseException):
            raise
        raise Exception(f'Could not find opf location in container.xml', e)


def find_path_to_opf_file(temp_path: Path) -> Path:
    container_content = _read_in_contents_of_container_file(temp_path)
    opf_location = _find_opf_location_in_container_content(container_content)
    opf_path = temp_path.joinpath(opf_location)
    if not opf_path.is_file():
        raise Exception(f'The opf file specified in the container.xml definition could not be found at specified location: [{opf_path}]')
    return opf_path


def add_manifest_entry_to_opf_file(temp_path: Path, opf_manifest_item: str):
    opf_file_path = find_path_to_opf_file(temp_path)
    print(f'Adding manifest item [{opf_manifest_item}] to opf file [{opf_file_path}]')
    with open(opf_file_path, 'r') as file:
        current_lines = file.readlines()
    opf_file_path.unlink()
    with open(opf_file_path, 'w') as file:
        for line in current_lines:
            if _MANIFEST_END_TAG in line:
                file.write(opf_manifest_item)
            file.write(line)
