from pathlib import Path

import unittest
from unittest.mock import Mock, patch

from repack.core.processors import FontResourceProcessor, ResourceProcessor

from ..util import fully_qualified_name


class FontResourceProcessorTests(unittest.TestCase):

    @patch(fully_qualified_name(ResourceProcessor))
    def test_process_font_file(self, mock_resource_processor: ResourceProcessor):
        processor = FontResourceProcessor(mock_resource_processor)

        temp_path = Path(__file__).absolute().parent

        expected = 'expected_value'
        mock_resource_processor.register_resource = Mock(return_value=Path(expected))

        actual = processor.process_font_file(temp_path)

        self.assertEqual(expected, actual)

        mock_resource_processor.register_resource.assert_called_once_with(
            temp_path,
            'Roboto-Light.ttf',
            '<item href="{}" id="{}_font" media-type="font/ttf"/>\n'
        )
