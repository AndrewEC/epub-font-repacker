from pathlib import Path
import uuid

from repack.opf import find_path_to_opf_file


_RESOURCE_FOLDER = 'resources'
_DESTINATION_RESOURCE_NAME_TEMPLATE = 'resource{}{}'


def get_path_to_resource(resource_name: str) -> Path:
    return Path(__file__).absolute().parent.joinpath(_RESOURCE_FOLDER).joinpath(resource_name)


def generate_destination_file_name(source_file: Path) -> str:
    formatted_uuid = str(uuid.uuid4()).replace('-', '')
    return _DESTINATION_RESOURCE_NAME_TEMPLATE.format(formatted_uuid, source_file.suffix)


def get_relative_joining_path(temp_path: Path, current_path: Path) -> str:
    next_path = current_path if current_path.is_dir() else current_path.parent
    if temp_path.name == next_path.name:
        return ''
    parent_folder_count = 0
    while temp_path.name != next_path.name:
        if next_path == next_path.parent:
            raise Exception(f'There is no common parent directory between: [{temp_path}] and [{current_path}]')
        next_path = next_path.parent
        parent_folder_count = parent_folder_count + 1
    return '../' * parent_folder_count


def get_relative_joining_path_to_manifest(temp_path: Path) -> str:
    opf_file_path = find_path_to_opf_file(temp_path)
    return get_relative_joining_path(temp_path, opf_file_path)
