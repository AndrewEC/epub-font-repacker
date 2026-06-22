from typing import List, Final, Dict
from pathlib import Path

import click

from repack.core.processors import EPUB_PROCESSOR_SINGLETON


_FONT_EXTENSIONS: Final[List[str]] = [
    '.ttf'
]


def _get_available_fonts() -> Dict[str, str]:
    resource_root = Path(__file__).absolute().parent.joinpath('core').joinpath('resources')
    font_files = [file for file in resource_root.iterdir() if file.suffix in _FONT_EXTENSIONS]
    return {file.stem.lower(): file.name for file in font_files}


_AVAILABLE_FONTS: Final[Dict[str, str]] = _get_available_fonts()


@click.command()
@click.argument('epub_file')
@click.argument('font', type=click.Choice(list(_AVAILABLE_FONTS.keys())))
@click.option(
    '--stack',
    '-s',
    is_flag=True,
    help='If provided the full stack trace of an error will be printed.'
)
def main(epub_file: str, font: str, stack: bool):
    """epub_file: The absolute or relative path to the epub file to repack."""

    try:
        EPUB_PROCESSOR_SINGLETON.process_epub_file(epub_file, _AVAILABLE_FONTS[font])
    except Exception as e:
        if stack:
            raise
        print(str(e))


if __name__ == '__main__':
    main()
