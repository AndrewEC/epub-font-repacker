from pathlib import Path

import unittest

from repack.core.paths import TempDirectoryFactory
from repack.core.errors import PathAlreadyExistsException


class TempDirectoryFactoryTests(unittest.TestCase):

    def test_create_temp_directory(self):
        temp_dir = Path(__file__).absolute().parent.joinpath('temp_path')
        with TempDirectoryFactory().create(temp_dir):
            self.assertTrue(temp_dir.is_dir())
        self.assertFalse(temp_dir.is_dir())

    def test_create_temp_directory_raises_error_if_directory_already_exists(self):
        temp_dir = Path(__file__).absolute().parent.joinpath('temp_path')
        factory = TempDirectoryFactory()
        with factory.create(temp_dir):
            self.assertTrue(temp_dir.is_dir())

            with self.assertRaises(PathAlreadyExistsException) as context:
                factory.create(temp_dir)
            self.assertTrue('A path could not be created because it already exists' in str(context.exception))

            self.assertTrue(temp_dir.is_dir())
        self.assertFalse(temp_dir.is_dir())
