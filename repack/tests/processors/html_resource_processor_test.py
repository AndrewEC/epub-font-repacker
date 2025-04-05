from pathlib import Path
import shutil

import unittest
from unittest.mock import patch, Mock

from repack.core.paths import JoiningPaths
from repack.core.processors import HtmlResouceProcessor

from ..util import fully_qualified_name


class HtmlResourceProcessorTests(unittest.TestCase):

    @patch(fully_qualified_name(JoiningPaths))
    def test_process_html_files(self, mock_joining_paths: JoiningPaths):
        html_resource_processor = HtmlResouceProcessor(mock_joining_paths)

        temp_path = Path(__file__).absolute().parent.joinpath('_temp')
        file_name = 'content.html'
        css_file_name = 'styles.css'

        mock_joining_paths.get_relative_joining_path = Mock(return_value='../../')

        try:
            self._create_test_resources(temp_path, file_name)

            html_resource_processor.process_html_files(temp_path, css_file_name)

            self._assert_test_resource(temp_path, file_name)

            mock_joining_paths.get_relative_joining_path.assert_called_once_with(temp_path, temp_path.joinpath(file_name))
        finally:
            self._delete_test_resources(temp_path)

    def _assert_test_resource(self, temp_path: Path, file_name: str):
        self.assertTrue(temp_path.is_dir())

        file_path = temp_path.joinpath(file_name)
        self.assertTrue(file_path.is_file())

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.assertEqual(3, len(lines))
            self.assertEqual('<link href="../../styles.css" rel="stylesheet" type="text/css"/>\n', lines[1])

    def _create_test_resources(self, temp_path: Path, file_name: str):
        temp_path.mkdir(parents=False, exist_ok=False)
        with open(temp_path.joinpath(file_name), 'w', encoding='utf-8') as file:
            file.write('<head>\n')
            file.write('</head>')

    def _delete_test_resources(self, temp_path: Path):
        if temp_path.is_dir:
            shutil.rmtree(temp_path)
