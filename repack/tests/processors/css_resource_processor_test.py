from pathlib import Path

import unittest
from unittest.mock import patch, Mock

from repack.core.processors import CssResourceProcessor, ResourceProcessor

from ..util import fully_qualified_name


_CSS_LINE = 'font-file - {} - font-file'


class CssResourceProcessorTests(unittest.TestCase):

    @patch(fully_qualified_name(ResourceProcessor))
    def test_process_css_file(self, mock_resource_processor: ResourceProcessor):
        font_file_name = 'font-file.ttf'
        resource_file = Path(__file__).absolute().parent.joinpath('_css_test_resource.css')
        try:
            mock_resource_processor.register_resource = Mock(return_value=resource_file)

            processor = CssResourceProcessor(mock_resource_processor)

            self._create_test_asset(resource_file)

            actual = processor.process_css_file(resource_file.parent, font_file_name)

            self._assert_test_asset(resource_file, font_file_name)
            self.assertEqual(resource_file.name, actual)
        finally:
            if resource_file.is_file():
                resource_file.unlink()

    def _create_test_asset(self, file_name: Path):
        with open(file_name, 'w', encoding='utf-8') as file:
            file.writelines([_CSS_LINE.format('{{font_file}}')])

    def _assert_test_asset(self, file_name: Path, font_file_name: str):
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        expected_line = _CSS_LINE.format(font_file_name)

        self.assertEqual(1, len(lines))
        self.assertEqual(expected_line, lines[0].strip())
