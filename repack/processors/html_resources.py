from typing import List
from pathlib import Path
import os

from repack.paths import get_relative_joining_path
from repack.progress_printer import Printer


_APPLICABLE_EXTENSIONS = [
    '.html',
    '.xhtml'
]


_CSS_LINK_TEMPLATE = '<link href="{}" rel="stylesheet" type="text/css"/>\n'
_END_HEAD_TAG = '</head>'


def _is_processable_file(file_path: Path) -> bool:
    return file_path.is_file() and file_path.suffix in _APPLICABLE_EXTENSIONS


def _list_all_processable_files(temp_path: Path) -> List[Path]:
    processable_files = []
    for root, dirs, files in os.walk(temp_path):
        for file in files:
            file_path = Path(root).joinpath(file)
            if _is_processable_file(file_path):
                processable_files.append(file_path)
    return processable_files


def _get_relative_link_to_css_file(temp_path: Path, file_path: Path, css_file_name: str) -> str:
    relative_prefix = get_relative_joining_path(temp_path, file_path)
    return f'{relative_prefix}{css_file_name}'


def process_html_files(temp_path: Path, css_file_name: str):
    """
    Iterates through all the xhtml and html files in the temp_path and adds a link tag at the end of the
    <head> tag that points to the css file previously processed and copied to the root of the temp_path.

    :param temp_path: The absolute path to the directory where the contents of the input epub file have been
        extracted to.
    :param css_file_name: The name of the css file processed by the css_resource.process_css_file function.
    """

    files = _list_all_processable_files(temp_path)
    file_count = len(files)
    print(f'Adding font style links to [{file_count}] content files')
    with Printer(file_count) as printer:
        for file_path in files:
            with printer.progress_tick(f'Processing: [{file_path.stem}]'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                file_path.unlink()
                with open(file_path, 'w', encoding='utf-8') as file:
                    for line in lines:
                        if _END_HEAD_TAG in line:
                            relative_css_link = _get_relative_link_to_css_file(temp_path, file_path, css_file_name)
                            file.write(_CSS_LINK_TEMPLATE.format(relative_css_link))
                        file.write(line)
