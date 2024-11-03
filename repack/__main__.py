import click
from pathlib import Path

import repack.processors as resource_processors
from repack.errors import EpubNotFoundException, PathAlreadyExistsException
from repack.paths import TempDirectory, get_temp_path
from .zipup import create_epub_zip, get_repacked_path, unzip_epub_contents_to_temp_dir


_TEMP_FOLDER_NAME_TEMPLATE = '_temp_{}'


def _process_epub_file(epub_file: str):
    epub_path = Path(epub_file).absolute()
    if not epub_path.is_file():
        raise EpubNotFoundException(epub_path)

    repacked_path = get_repacked_path(epub_path)
    if repacked_path.is_file():
        raise PathAlreadyExistsException(repacked_path)

    temp_path = get_temp_path(epub_path)

    with TempDirectory(temp_path):
        print(f'Processing epub file: [{epub_path}]')

        unzip_epub_contents_to_temp_dir(epub_path, temp_path)

        font_file_name = resource_processors.process_font_file(temp_path)
        css_file_name = resource_processors.process_css_file(temp_path, font_file_name)
        resource_processors.process_html_files(temp_path, css_file_name)

        create_epub_zip(epub_path, temp_path)


@click.command()
@click.argument('epub_file')
@click.option(
    '--stack',
    '-s',
    is_flag=True,
    help='If provided the full stack trace of an error will be printed.'
)
def main(epub_file: str, stack: bool):
    """epub_file: The absolute or relative path to the epub file to repack."""

    try:
        _process_epub_file(epub_file)
    except Exception as e:
        if stack:
            raise
        print(str(e))


if __name__ == '__main__':
    main()
