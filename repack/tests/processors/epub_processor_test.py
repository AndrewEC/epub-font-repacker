from pathlib import Path
import shutil

import unittest
from unittest.mock import patch, Mock

from repack.core.processors import (
    HtmlResouceProcessor,
    FontResourceProcessor,
    CssResourceProcessor,
    EpubProcessor
)
from repack.core.paths import (
    TempDirectoryFactory,
    ResourcePaths
)
from repack.core.util import ZipUp

from ..util import fully_qualified_name


class EpubProcessorTest(unittest.TestCase):

    @patch(fully_qualified_name(ResourcePaths))
    @patch(fully_qualified_name(TempDirectoryFactory))
    @patch(fully_qualified_name(ZipUp))
    @patch(fully_qualified_name(CssResourceProcessor))
    @patch(fully_qualified_name(FontResourceProcessor))
    @patch(fully_qualified_name(HtmlResouceProcessor))
    def test_process_epub_file(self,
                               mock_html_resource_processor: HtmlResouceProcessor,
                               mock_font_resource_processor: FontResourceProcessor,
                               mock_css_resource_processor: CssResourceProcessor,
                               mock_zip_up: ZipUp,
                               mock_temp_directory_factory: TempDirectoryFactory,
                               mock_resource_paths: ResourcePaths):

        epub_processor = EpubProcessor(
            mock_font_resource_processor,
            mock_css_resource_processor,
            mock_html_resource_processor,
            mock_zip_up,
            mock_temp_directory_factory,
            mock_resource_paths
        )

        epub_path = Path(__file__).absolute().parent.joinpath('_temp').joinpath('test.epub')

        repacked_path = epub_path.parent.joinpath('test-repacked.epub')
        mock_zip_up.get_repacked_path = Mock(return_value=repacked_path)

        temp_path = epub_path.parent
        mock_resource_paths.get_temp_path = Mock(return_value=temp_path)

        temp_directory = Mock(__enter__=Mock(), __exit__=Mock())
        mock_temp_directory_factory.create = Mock(return_value=temp_directory)

        mock_zip_up.unzip_epub_contents_to_temp_dir = Mock()

        font_file_name = 'font-file.woff'
        mock_font_resource_processor.process_font_file = Mock(return_value=font_file_name)

        css_file_name = 'styles.css'
        mock_css_resource_processor.process_css_file = Mock(return_value=css_file_name)

        mock_html_resource_processor.process_html_files = Mock()

        mock_zip_up.create_epub_zip = Mock()

        try:
            self._create_test_resource(epub_path)

            epub_processor.process_epub_file(str(epub_path))

            mock_zip_up.unzip_epub_contents_to_temp_dir.assert_called_once_with(epub_path, temp_path)
            mock_font_resource_processor.process_font_file.assert_called_once_with(temp_path)
            mock_css_resource_processor.process_css_file.assert_called_once_with(temp_path, font_file_name)
            mock_html_resource_processor.process_html_files.assert_called_once_with(temp_path, css_file_name)
            mock_zip_up.create_epub_zip.assert_called_once_with(epub_path, temp_path)

            temp_directory.__enter__.assert_called_once()
            temp_directory.__exit__.assert_called_once()
        finally:
            self._remove_test_resource(epub_path)

    def _create_test_resource(self, file_path: Path):
        file_path.parent.mkdir(parents=False, exist_ok=False)
        with open(file_path, 'w', encoding='utf-8'):
            pass

    def _remove_test_resource(self, file_path: Path):
        if file_path.parent.is_dir():
            shutil.rmtree(file_path.parent)
