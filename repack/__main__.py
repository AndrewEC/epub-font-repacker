import click
from pathlib import Path
from zipfile import ZipFile

import repack.processors as resource_processors
from repack.errors import EpubNotFoundException
from repack.paths import TempDirectory, get_temp_path
from .zipup import create_epub_zip


_TEMP_FOLDER_NAME_TEMPLATE = '_temp_{}'


def _unzip_epub_contents_to_temp_dir(epub_path: Path, temp_path: Path):
    print(f'Unzipping contents to temp folder: [{temp_path}]')
    with ZipFile(epub_path, 'r') as zip_file:
        zip_file.extractall(temp_path)


def _process_epub_file(epub_file: str):
    epub_path = Path(epub_file)
    if not epub_path.is_file():
        raise EpubNotFoundException(epub_path)

    temp_path = get_temp_path(epub_path)

    with TempDirectory(temp_path):
        print(f'Processing epub file: [{epub_path}]')

        _unzip_epub_contents_to_temp_dir(epub_path, temp_path)
        print()

        font_file_name = resource_processors.process_font_file(temp_path)
        print()
        css_file_name = resource_processors.process_css_file(temp_path, font_file_name)
        print()
        resource_processors.process_html_files(temp_path, css_file_name)
        print()

        create_epub_zip(epub_path, temp_path)
        print()


@click.command()
@click.argument('epub_file')
def main(epub_file: str):
    """epub_file: The absolute or relative path to the epub file to modify."""

    try:
        _process_epub_file(epub_file)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
