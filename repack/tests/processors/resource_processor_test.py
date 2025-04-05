from pathlib import Path
import shutil

import unittest
from unittest.mock import patch, Mock

from repack.core.processors import ResourceProcessor
from repack.core.paths import ResourcePaths, JoiningPaths
from repack.core.util import Opf

from ..util import fully_qualified_name


class ResourceProcessorTests(unittest.TestCase):

    @patch(fully_qualified_name(Opf))
    @patch(fully_qualified_name(JoiningPaths))
    @patch(fully_qualified_name(ResourcePaths))
    def test_register_resource(self,
                               mock_resource_paths: ResourcePaths,
                               mock_joining_paths: JoiningPaths,
                               mock_opf: Opf):

        temp_path = Path(__file__).absolute().parent.joinpath('temp')
        resource_name = 'resource_name.css'

        resource_path = temp_path.joinpath(resource_name)
        mock_resource_paths.get_path_to_resource = Mock(return_value=resource_path)

        destination_file_name = '123_resource_name.css'
        mock_resource_paths.generate_destination_file_name = Mock(return_value=destination_file_name)

        joining_path = '../../'
        mock_joining_paths.get_relative_joining_path_to_manifest = Mock(return_value=joining_path)

        mock_opf.add_manifest_entry_to_opf_file = Mock()

        processor = ResourceProcessor(mock_opf, mock_resource_paths, mock_joining_paths)

        self._create_test_resources(temp_path, resource_name)

        try:
            actual = processor.register_resource(temp_path, resource_name, 'manifest {} {}')

            destination_path = temp_path.joinpath(destination_file_name)
            self.assertTrue(destination_path.is_file())

            self.assertEqual(destination_path, actual)

            mock_resource_paths.get_path_to_resource.assert_called_once_with(resource_name)
            mock_resource_paths.generate_destination_file_name.assert_called_once_with(resource_path)
            mock_joining_paths.get_relative_joining_path_to_manifest.assert_called_once_with(temp_path)
            mock_opf.add_manifest_entry_to_opf_file.assert_called_once_with(
                temp_path,
                'manifest ../../123_resource_name.css 123_resource_name'
            )
        finally:
            self._delete_resource_resources(temp_path)

    def _create_test_resources(self, temp_path: Path, resource_name: str):
        temp_path.mkdir(parents=False, exist_ok=False)
        with open(temp_path.joinpath(resource_name), 'w', encoding='utf-8'):
            pass

    def _delete_resource_resources(self, temp_path: Path):
        if temp_path.is_dir():
            shutil.rmtree(temp_path)
