from pathlib import Path

from .process_resource import process_resource


_FONT_FILE_NAME = 'Roboto-Light.ttf'
_FONT_MANIFEST_ENTRY_TEMPLATE = '<item href="{}" id="{}_font" media-type="font/ttf"/>\n'


def process_font_file(temp_path: Path) -> str:
    """
    Copies the font file from the resources folder to the root of the temp_path.

    :param temp_path: The absolute path to the directory where the contents of the input epub file have been
        extracted to.
    :return: The absolute path to the font file copied to the
    """

    print('Copying font file to temp directory')
    return process_resource(temp_path, _FONT_FILE_NAME, _FONT_MANIFEST_ENTRY_TEMPLATE).name
