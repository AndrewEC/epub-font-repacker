from pathlib import Path

from .resource_processor import ResourceProcessor, RESOURCE_PROCESSOR_SINGLETON


_FONT_FILE_NAME = 'Roboto-Light.ttf'
_FONT_MANIFEST_ENTRY_TEMPLATE = '<item href="{}" id="{}_font" media-type="font/ttf"/>\n'


class FontResourceProcessor:

    def __init__(self, resource_processor: ResourceProcessor = RESOURCE_PROCESSOR_SINGLETON):
        self._resource_processor = resource_processor

    def process_font_file(self, temp_path: Path) -> str:
        """
        Copies the font file from the resources folder to the root of the temp_path and adds an entry for the file
        in the main OPF file.

        :param temp_path: The absolute path to the directory where the contents of the input epub file have been
            extracted to.
        :return: The absolute path to the font file copied to the
        """

        print(f'Adding font file: [{_FONT_FILE_NAME}]')
        return self._resource_processor.register_resource(temp_path, _FONT_FILE_NAME, _FONT_MANIFEST_ENTRY_TEMPLATE).name


FONT_RESOURCE_PROCESSOR_SINGLETON = FontResourceProcessor()
