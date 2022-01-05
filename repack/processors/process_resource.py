from pathlib import Path
import shutil
from repack.paths import get_path_to_resource, generate_destination_file_name, get_relative_joining_path_to_manifest
from repack.opf import add_manifest_entry_to_opf_file


def process_resource(temp_path, resource_name: str, manifest_template: str) -> Path:
    resource_path = get_path_to_resource(resource_name)
    if not resource_path.is_file():
        raise Exception(f'The required resource could not be found at: [{resource_path}]')

    destination_file_name = generate_destination_file_name(resource_path)
    destination_file_path = temp_path.joinpath(destination_file_name)
    relative_link_location = f'{get_relative_joining_path_to_manifest(temp_path)}{destination_file_name}'

    opf_manifest_entry = manifest_template.format(relative_link_location, destination_file_path.stem)
    add_manifest_entry_to_opf_file(temp_path, opf_manifest_entry)

    shutil.copy(resource_path, destination_file_path)

    return destination_file_path
