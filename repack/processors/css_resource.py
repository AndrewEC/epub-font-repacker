from pathlib import Path

from .process_resource import process_resource


_CSS_FILE_NAME = 'custom-font.css'
_CSS_MANIFEST_ENTRY_TEMPLATE = '<item href="{}" id="{}_css" media-type="text/css"/>\n'
_CSS_FONT_FILE_PLACEHOLDER = '{{font_file}}'


def _replace_placeholder_with_path_to_font_file(font_file_name: str, css_file_path: Path):
    with open(css_file_path, 'r') as file:
        lines = file.readlines()
    css_file_path.unlink()
    content = '\n'.join([line.replace(_CSS_FONT_FILE_PLACEHOLDER, font_file_name) for line in lines])
    with open(css_file_path, 'w') as file:
        file.write(content)


def process_css_file(temp_path: Path, font_file_name: str) -> str:
    print('Copying css file to temp directory')

    destination_css_file_path = process_resource(temp_path, _CSS_FILE_NAME, _CSS_MANIFEST_ENTRY_TEMPLATE)

    _replace_placeholder_with_path_to_font_file(font_file_name, destination_css_file_path)

    return destination_css_file_path.name
