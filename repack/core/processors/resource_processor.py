from pathlib import Path
import shutil

from repack.core.paths import ResourcePaths, RESOURCE_PATHS_SINGLETON, JoiningPaths, JOINING_PATHS_SINGLETON
from repack.core.util import Opf, OPF_SINGLETON
from repack.core.errors import MissingResourceException


class ResourceProcessor:

    def __init__(self, opf: Opf = OPF_SINGLETON,
                 resource_paths: ResourcePaths = RESOURCE_PATHS_SINGLETON,
                 joining_paths: JoiningPaths = JOINING_PATHS_SINGLETON):

        self._opf = opf
        self._resource_paths = resource_paths
        self._joining_paths = joining_paths

    def register_resource(self, temp_path: Path, resource_name: str, manifest_template: str) -> Path:
        """
        This function will look for a resource under the resources folder, generate a random uuid like name for the
        file, copy it to the root of the temp_path, and insert the manifest_template at the tail end of the manifest
        section of the OPF file located under the path specified by temp_path.

        :param temp_path: The absolute path to the directory where the contents of the input epub file have been
            extracted to.
        :param resource_name: The name of the file under the resources folder we are processing and copying to the
            temp_path.
        :param manifest_template: An XML template to be updated and inserted in the manifest, OPF, file to create a
            reference in the manifest to the new file this function will introduce to the temp_path.
        :return: The path to the file written at the end of this function.
        """

        resource_path = self._resource_paths.get_path_to_resource(resource_name)
        if not resource_path.is_file():
            raise MissingResourceException(resource_path)

        destination_file_name = self._resource_paths.generate_destination_file_name(resource_path)
        destination_file_path = temp_path.joinpath(destination_file_name)
        manifest_joining_paths = self._joining_paths.get_relative_joining_path_to_manifest(temp_path)
        relative_link_location = f'{manifest_joining_paths}{destination_file_name}'

        print(f'Registering resource [{resource_name}] in manifest with name [{destination_file_name}]')

        opf_manifest_entry = manifest_template.format(relative_link_location, destination_file_path.stem)
        self._opf.add_manifest_entry_to_opf_file(temp_path, opf_manifest_entry)

        shutil.copy(resource_path, destination_file_path)

        return destination_file_path


RESOURCE_PROCESSOR_SINGLETON = ResourceProcessor()
