from pathlib import Path
import shutil

import unittest

from repack.core.util import ZipUp


class ZipUpTests(unittest.TestCase):

    def test_get_repacked_path(self):
        input_path = Path(__file__).absolute().parent.joinpath('_temp').joinpath('test.epub')
        expected_path = input_path.parent.joinpath('test - Repacked.epub')

        zipup = ZipUp()

        self.assertEqual(expected_path, zipup.get_repacked_path(input_path))

    def test_create_epub_zip(self):
        zipup = ZipUp()

        epub_path = self._get_test_epub_path()

        temp_path = Path(__file__).absolute().parent.joinpath('_temp')
        repacked_path = zipup.get_repacked_path(epub_path)

        try:
            temp_path.mkdir(parents=False, exist_ok=False)
            shutil.copytree(epub_path.parent, temp_path, dirs_exist_ok=True)

            zipup.create_epub_zip(epub_path, temp_path)

            self.assertTrue(repacked_path.is_file(), 'Repacked path could not be found.')
        finally:
            if temp_path.is_dir():
                shutil.rmtree(temp_path)

            if repacked_path.is_file():
                repacked_path.unlink()

    def _get_test_epub_path(self) -> Path:
        asset_path = (Path(__file__).absolute()
                      .parent
                      .joinpath('zipup_test_assets'))

        if not asset_path.is_dir():
            raise Exception(f'Could not find test assets in expected location of [{asset_path}].')

        return asset_path.joinpath('test.epub')
