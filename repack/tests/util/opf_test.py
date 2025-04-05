import shutil
from pathlib import Path

import unittest

from repack.core.util import Opf


class OpfTests(unittest.TestCase):

    def test_find_path_to_opf_file(self):
        temp_path = self._get_source_path()
        expected_path = temp_path.joinpath('OEBPS').joinpath('content.opf')

        opf = Opf()

        self.assertEqual(expected_path, opf.find_path_to_opf_file(temp_path))

    def test_add_manifest_entry_to_opf_file(self):
        source_path = self._get_source_path()
        temp_path = source_path.parent.joinpath('_temp')
        manifest_path = temp_path.joinpath('OEBPS').joinpath('content.opf')
        manifest_item = '<item href="./styles.css" id="Test" media-type="text/css" />'

        try:
            temp_path.mkdir(parents=False, exist_ok=False)
            shutil.copytree(source_path, temp_path, dirs_exist_ok=True)

            Opf().add_manifest_entry_to_opf_file(temp_path, manifest_item)

            self._assert_resource_updated(manifest_path, manifest_item)
        finally:
            if temp_path.is_dir():
                shutil.rmtree(temp_path)

    def _assert_resource_updated(self, file_path: Path, expected_line: str):
        self.assertTrue(file_path.is_file())

        with open(file_path, 'r', encoding='utf-8') as file:
            contains_line = any([line for line in file.readlines() if expected_line in line])
            self.assertTrue(contains_line, f'content.opf did not contain expected new line [{expected_line}].')

    def _get_source_path(self) -> Path:
        temp_path = Path(__file__).absolute().parent.joinpath('opf_test_assets')
        if not temp_path.is_dir():
            raise Exception(f'Could not find test assets at expected location of: [{temp_path}].')
        return temp_path
