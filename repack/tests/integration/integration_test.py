from typing import List
import shutil
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree
import re

import unittest

from repack.core.processors import EPUB_PROCESSOR_SINGLETON


class IntegrationTest(unittest.TestCase):

    _XHTML_LINK_PATTERN = '^<link href="\\.\\.\\/resource(?:[0-9]|[a-z]){8}\\.css" rel="stylesheet" type="text\\/css"\\/>'

    def test_repack(self):
        test_data_path = Path(__file__).absolute().parent.joinpath('test_data')

        epub_path = test_data_path.joinpath('test_epub.epub')
        if not epub_path.is_file():
            raise Exception(f'Could not find test epub file in expected location of: [{epub_path}].')

        repacked_path = test_data_path.joinpath('test_epub - Repacked.epub')

        try:
            EPUB_PROCESSOR_SINGLETON.process_epub_file(str(epub_path))

            self._assert_repacked_epub(repacked_path)
        finally:
            if repacked_path.is_file():
                repacked_path.unlink()

    def _assert_repacked_epub(self, repacked_path: Path):
        self.assertTrue(repacked_path.is_file(), f'Repacked epub must be in location [{repacked_path}].')

        temp_path = repacked_path.parent.joinpath('_temp')

        try:
            temp_path.mkdir(parents=False, exist_ok=False)

            with ZipFile(repacked_path, 'r') as zip_file:
                zip_file.extractall(temp_path)

            temp_files = list(temp_path.iterdir())

            css_resource = self._assert_contains_file(temp_files, 'resource', 'css')
            font_resource = self._assert_contains_file(temp_files, 'resource', 'ttf')

            self._assert_entries_in_opf(temp_path, font_resource, css_resource)
            self._assert_chapter_contains_style_line(temp_path, css_resource)
        finally:
            if temp_path.is_dir():
                shutil.rmtree(temp_path)

    def _assert_contains_file(self, files: List[Path], prefix: str, suffix: str) -> str:
        def matches(file_name: str) -> bool:
            return file_name.startswith(prefix) and file_name.endswith(suffix) and len(file_name) == 20

        matching_file = next((file.name for file in files if matches(file.name)), None)

        self.assertIsNotNone(matching_file, f'No file in repacked epub starts with [{prefix}] and ends with [{suffix}].')

        return matching_file if matching_file is not None else ''

    def _assert_entries_in_opf(self, temp_path: Path, font_resource: str, css_resource: str):
        opf_path = temp_path.joinpath('package.opf')
        self.assertTrue(opf_path.is_file(), f'Expected opf to be in location of [{opf_path}].')

        with open(opf_path, 'r', encoding='utf-8') as file:
            contents = ''.join(file.readlines())

        manifest_items = ElementTree.fromstring(contents).findall('.//{*}item')
        self._assert_manifest_entry(manifest_items, font_resource)  # type: ignore
        self._assert_manifest_entry(manifest_items, css_resource)  # type: ignore

    def _assert_manifest_entry(self, manifest_items: List[ElementTree.Element[str]], href_target: str):
        matching_item = next((item for item in manifest_items if item.attrib.get('href') == href_target), None)
        self.assertIsNotNone(matching_item, f'Expected manifest to contain one entry with a href of [{href_target}].')

    def _assert_chapter_contains_style_line(self, temp_path: Path, css_resource: str):
        chapter_file = temp_path.joinpath('chapters').joinpath('Chapter1.xhtml')
        self.assertTrue(chapter_file.is_file(), f'Expected chapter file to be in location of [{chapter_file}]')

        with open(chapter_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        expression = re.compile(IntegrationTest._XHTML_LINK_PATTERN)

        matching_link = next((line for line in lines if expression.match(line)), None)
        self.assertIsNotNone(matching_link, f'Expected chapter file to contain link to [{css_resource}].')
