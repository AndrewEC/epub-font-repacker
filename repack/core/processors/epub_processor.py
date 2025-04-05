from pathlib import Path

from repack.core.processors import (
    HtmlResouceProcessor,
    HTML_RESOURCE_PROCESSOR_SINGLETON,

    FontResourceProcessor,
    FONT_RESOURCE_PROCESSOR_SINGLETON,

    CssResourceProcessor,
    CSS_RESOURCE_PROCESSOR_SINGLETON
)
from repack.core.errors import EpubNotFoundException, PathAlreadyExistsException
from repack.core.paths import (
    TEMP_DIRECTORY_FACTORY_SINGLETON,
    TempDirectoryFactory,
    ResourcePaths,
    RESOURCE_PATHS_SINGLETON
)
from repack.core.util import ZipUp, ZIP_UP_SINGLETON


class EpubProcessor:

    def __init__(self,
                 font_resource_processor: FontResourceProcessor = FONT_RESOURCE_PROCESSOR_SINGLETON,
                 css_resource_processor: CssResourceProcessor = CSS_RESOURCE_PROCESSOR_SINGLETON,
                 html_resource_processor: HtmlResouceProcessor = HTML_RESOURCE_PROCESSOR_SINGLETON,
                 zip_up: ZipUp = ZIP_UP_SINGLETON,
                 temp_directory_factory: TempDirectoryFactory = TEMP_DIRECTORY_FACTORY_SINGLETON,
                 resource_paths: ResourcePaths = RESOURCE_PATHS_SINGLETON):

        self._font_resource_processor = font_resource_processor
        self._css_resouce_processor = css_resource_processor
        self._html_resource_processor = html_resource_processor
        self._zip_up = zip_up
        self._temp_directory_factory = temp_directory_factory
        self._resource_paths = resource_paths

    def process_epub_file(self, epub_file: str):
        """
        The 'entry point' of the application that orchestrates the flow of extract, updating,
        and repacking the epub file.

        :param epub_file: The string representation of the path to the epub file to
            be updated.
        """

        epub_path = Path(epub_file).absolute()
        if not epub_path.is_file():
            raise EpubNotFoundException(epub_path)

        repacked_path = self._zip_up.get_repacked_path(epub_path)
        if repacked_path.is_file():
            raise PathAlreadyExistsException(repacked_path)

        temp_path = self._resource_paths.get_temp_path(epub_path)

        with self._temp_directory_factory.create(temp_path):
            print(f'Processing epub file: [{epub_path}]')

            self._zip_up.unzip_epub_contents_to_temp_dir(epub_path, temp_path)

            font_file_name = self._font_resource_processor.process_font_file(temp_path)
            css_file_name = self._css_resouce_processor.process_css_file(temp_path, font_file_name)
            self._html_resource_processor.process_html_files(temp_path, css_file_name)

            self._zip_up.create_epub_zip(epub_path, temp_path)


EPUB_PROCESSOR_SINGLETON = EpubProcessor()
