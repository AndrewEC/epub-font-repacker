from typing import List
from pathlib import Path
import os

from repack.core.paths import JoiningPaths, JOINING_PATHS_SINGLETON
from repack.core.util import read_and_unlink


_APPLICABLE_EXTENSIONS = [
    '.html',
    '.xhtml'
]


_CSS_LINK_TEMPLATE = '<link href="{}" rel="stylesheet" type="text/css"/>\n'
_END_HEAD_TAG = '</head>'


class HtmlResouceProcessor:

    def __init__(self, joining_paths: JoiningPaths = JOINING_PATHS_SINGLETON):
        self._joining_paths = joining_paths

    def process_html_files(self, temp_path: Path, css_file_name: str):
        """
        Iterates through all the xhtml and html files in the temp_path and adds a link tag at the end of the
        <head> tag that points to the css file previously processed and copied to the root of the temp_path.

        :param temp_path: The absolute path to the directory where the contents of the input epub file have been
            extracted to.
        :param css_file_name: The name of the css file processed by the css_resource.process_css_file function.
        """

        files = self._list_all_processable_files(temp_path)
        file_count = len(files)
        print(f'Adding font style links to [{file_count}] content files.')
        for file_path in files:
            lines = read_and_unlink(file_path)
            self._write_html_file_with_css_link(file_path, lines, temp_path, css_file_name)

    def _is_processable_file(self, file_path: Path) -> bool:
        return file_path.is_file() and file_path.suffix in _APPLICABLE_EXTENSIONS

    def _list_all_processable_files(self, temp_path: Path) -> List[Path]:
        processable_files = []
        for root, _, files in os.walk(temp_path):
            for file in files:
                file_path = Path(root).joinpath(file)
                if self._is_processable_file(file_path):
                    processable_files.append(file_path)
        return processable_files

    def _get_relative_link_to_css_file(self, temp_path: Path, file_path: Path, css_file_name: str) -> str:
        relative_prefix = self._joining_paths.get_relative_joining_path(temp_path, file_path)
        return f'{relative_prefix}{css_file_name}'

    def _write_html_file_with_css_link(self, file_path: Path, lines: List[str], temp_path: Path, css_file_name: str):
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if _END_HEAD_TAG in line:
                    relative_css_link = self._get_relative_link_to_css_file(temp_path, file_path, css_file_name)
                    file.write(_CSS_LINK_TEMPLATE.format(relative_css_link))
                file.write(line)


HTML_RESOURCE_PROCESSOR_SINGLETON = HtmlResouceProcessor()
