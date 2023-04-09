import click
from pathlib import Path
import shutil
from zipfile import ZipFile

import repack.processors as resource_processors
from repack.errors import EpubNotFoundException
from .zipup import create_epub_zip


_TEMP_FOLDER_NAME_TEMPLATE = '_temp_{}'


def _unzip_epub_contents_to_temp_dir(epub_path: Path, temp_path: Path):
    print(f'Unzipping contents to temp folder: [{temp_path}]')
    if temp_path.is_dir():
        shutil.rmtree(temp_path)
    with ZipFile(epub_path, 'r') as zip_file:
        zip_file.extractall(temp_path)


def _process_epub_file(epub_path: Path, temp_path: Path):
    if not epub_path.is_file():
        raise EpubNotFoundException(epub_path)

    print(f'Processing epub file: [{epub_path}]')

    _unzip_epub_contents_to_temp_dir(epub_path, temp_path)

    font_file_name = resource_processors.process_font_file(temp_path)

    css_file_name = resource_processors.process_css_file(temp_path, font_file_name)

    resource_processors.process_html_files(temp_path, css_file_name)

    create_epub_zip(epub_path, temp_path)


@click.command()
@click.argument('epub_file')
def main(epub_file: str):
    """epub_file: The absolute or relative path to the epub file to modify."""

    epub_path = Path(epub_file)
    temp_path = epub_path.parent.joinpath(_TEMP_FOLDER_NAME_TEMPLATE.format(epub_path.stem))

    try:
        _process_epub_file(epub_path, temp_path)
    except Exception as e:
        print(str(e))
    finally:
        try:
            shutil.rmtree(temp_path)
        except:
            print(f'Could not delete temp path at: [{temp_path}]')
            print('It is safe to manually delete the temp path.')


if __name__ == '__main__':
    main()
