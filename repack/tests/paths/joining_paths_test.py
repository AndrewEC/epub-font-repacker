from pathlib import Path

import unittest
from unittest.mock import patch, Mock

from repack.core.paths import JoiningPaths
from repack.core.util import Opf

from ..util import fully_qualified_name


class JoiningPathsTests(unittest.TestCase):

    def test_get_relative_joining_path(self):
        joining_paths = JoiningPaths()

        child_folder = Path(__file__).absolute().parent
        parent_folder = child_folder.parent.parent

        actual = joining_paths.get_relative_joining_path(parent_folder, child_folder)
        self.assertEqual('../../', actual)

    @patch(fully_qualified_name(Opf))
    def test_get_relative_joining_path_to_manifest(self, mock_opf: Opf):
        joining_paths = JoiningPaths(mock_opf)

        root_path = Path(__file__).absolute().parent
        opf_path = root_path.parent
        temp_path = root_path.parent.parent.parent

        mock_opf.find_path_to_opf_file = Mock(return_value=opf_path)

        actual = joining_paths.get_relative_joining_path_to_manifest(temp_path)
        self.assertEqual('../../', actual)

        mock_opf.find_path_to_opf_file.assert_called_once_with(temp_path)
