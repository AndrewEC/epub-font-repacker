from pathlib import Path

from .process_resource import process_resource


_FONT_FILE_NAME = 'Roboto-Light.ttf'
_FONT_MANIFEST_ENTRY_TEMPLATE = '<item href="{}" id="{}_font" media-type="font/ttf"/>\n'


def process_font_file(temp_path: Path) -> str:
    print('Copying font file to temp directory')
    return process_resource(temp_path, _FONT_FILE_NAME, _FONT_MANIFEST_ENTRY_TEMPLATE).name
