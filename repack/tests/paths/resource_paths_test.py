from pathlib import Path

import unittest

from repack.core.paths import ResourcePaths


class ResourcePathsTests(unittest.TestCase):

    def test_get_temp_path(self):
        input_path = Path(__file__)
        path = ResourcePaths().get_temp_path(input_path)
        self.assertEqual(
            "C:\\Stuff\\Programming\\Python\\epub-font-repacker\\repack\\tests\\paths\\_temp_resource_paths_test".upper(),
            str(path).upper()
        )

    def test_get_path_to_resource(self):
        resource_name = 'test_resource'
        path = ResourcePaths().get_path_to_resource(resource_name)
        self.assertEqual(
            'C:\\Stuff\\Programming\\Python\\epub-font-repacker\\repack\\core\\resources\\test_resource'.upper(),
            str(path).upper()
        )

    def test_generate_destination_file_name(self):
        file_name = ResourcePaths().generate_destination_file_name(Path(__file__))
        self.assertTrue(file_name.startswith('resource'), 'Expected file_name to start with \'resource\'.')
        self.assertTrue(file_name.endswith('.py'), 'Expected file_name to end with \'.py\'.')
        self.assertEqual(19, len(file_name))
