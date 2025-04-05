from pathlib import Path

from repack.core.util import read_and_unlink
from .resource_processor import ResourceProcessor, RESOURCE_PROCESSOR_SINGLETON


_CSS_FILE_NAME = 'custom-font.css'
_CSS_MANIFEST_ENTRY_TEMPLATE = '<item href="{}" id="{}_css" media-type="text/css"/>\n'
_CSS_FONT_FILE_PLACEHOLDER = '{{font_file}}'


class CssResourceProcessor:

    def __init__(self, resource_processor: ResourceProcessor = RESOURCE_PROCESSOR_SINGLETON):
        self._resource_processor = resource_processor

    def process_css_file(self, temp_path: Path, font_file_name: str) -> str:
        """
        Processes the css file located under the resources directory.

        This will take the css file, replace the {{font_file}} placeholder with the value of font_file_name, and write the
        updated css file to the root of the temp_path.

        :param temp_path: The absolute path to the directory where the contents of the input epub file have been
            extracted to.
        :param font_file_name: The name of the font file to be used throughout the epub file.
        """

        print('Adding CSS file.')

        destination_css_file_path = (self._resource_processor
                                     .register_resource(temp_path, _CSS_FILE_NAME, _CSS_MANIFEST_ENTRY_TEMPLATE))

        self._replace_placeholder_with_path_to_font_file(font_file_name, destination_css_file_path)

        return destination_css_file_path.name

    def _replace_placeholder_with_path_to_font_file(self, font_file_name: str, css_file_path: Path):
        lines = read_and_unlink(css_file_path)
        content = '\n'.join([line.replace(_CSS_FONT_FILE_PLACEHOLDER, font_file_name) for line in lines])
        with open(css_file_path, 'w', encoding='utf-8') as file:
            file.write(content)


CSS_RESOURCE_PROCESSOR_SINGLETON = CssResourceProcessor()
