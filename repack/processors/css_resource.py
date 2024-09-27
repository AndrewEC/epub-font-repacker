from pathlib import Path

from .process_resource import register_resource


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
    """
    Processes the css file located under the resources directory.

    This will take the css file, replace the {{font_file}} placeholder with the value of font_file_name, and write the
    updated css file to the root of the temp_path.

    :param temp_path: The absolute path to the directory where the contents of the input epub file have been
        extracted to.
    :param font_file_name: The name of the font file to be used throughout the epub file.
    """

    print('Adding CSS file.')

    destination_css_file_path = register_resource(temp_path, _CSS_FILE_NAME, _CSS_MANIFEST_ENTRY_TEMPLATE)

    _replace_placeholder_with_path_to_font_file(font_file_name, destination_css_file_path)

    return destination_css_file_path.name
