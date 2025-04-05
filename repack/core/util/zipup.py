import os
from typing import List
from pathlib import Path
from zipfile import ZipFile, ZIP_STORED

from repack.core.errors import MissingMimetypeFileException


_MIMETYPE_FILE = 'mimetype'
_REPACKED_EPUB_NAME_TEMPLATE = '{} - Repacked.epub'


class ZipUp:

    def get_repacked_path(self, epub_path: Path) -> Path:
        """
        Gets the full path where the repacked epub file will be written to.

        :param epub_path: The path of the epub that is going to be repacked.
        :return: The full path where the repacked epub file will be written to.
        """
        repacked_name = _REPACKED_EPUB_NAME_TEMPLATE.format(epub_path.stem)
        return epub_path.parent.joinpath(repacked_name)

    def unzip_epub_contents_to_temp_dir(self, epub_path: Path, temp_path: Path):
        print(f'Unzipping contents to temp folder: [{temp_path}]')
        with ZipFile(epub_path, 'r') as zip_file:
            zip_file.extractall(temp_path)

    def create_epub_zip(self, epub_path: Path, temp_path: Path):
        """
        This will zip up all the files located under the temp_path into a single epub file and place the epub file in the
        same folder as the epub file specified in epub_path.

        This will also ensure that the mimetype file is the first entry in the epub zip.

        :param epub_path: The absolute path of the epub file that will be generated after this method has been executed.
        :param temp_path: The path to the files that will be added to the epub file.
        """
        repacked_path = self.get_repacked_path(epub_path)

        files_to_archive = self._get_sorted_list_of_files_to_archive(temp_path)

        print(f'Zipping [{len(files_to_archive)}] files into repacked epub.')
        with ZipFile(repacked_path, 'w', ZIP_STORED) as zippy:
            for file in files_to_archive:
                zippy.write(file, self._get_archive_file_name(temp_path, file))

        print(f'\nRepacked epub can be found at: [{repacked_path}]')

    def _get_files_to_archive(self, temp_path: Path) -> List[Path]:
        all_files = []
        for root, _, files in os.walk(temp_path):
            for file_name in files:
                all_files.append(Path(root).joinpath(file_name))
        return all_files

    def _get_sorted_list_of_files_to_archive(self, temp_path: Path) -> List[Path]:
        """
        The reason this method exists is to ensure that we adhere to the Epub 3 specification which stipulates the
        mimetype file needs to be the first entry in the epub zip file.

        This will essentially get a list of all files to archive, look for the mimetype file, and move said file to
        be the first element in the list of files this function will return.
        """

        files_to_archive = self._get_files_to_archive(temp_path)
        index_of_mimetype_file = next((index for index, file_path in enumerate(files_to_archive) if file_path.name == _MIMETYPE_FILE), -1)
        if index_of_mimetype_file == -1:
            raise MissingMimetypeFileException()
        mime_type_file = files_to_archive.pop(index_of_mimetype_file)
        files_to_archive.insert(0, mime_type_file)
        return files_to_archive

    def _get_archive_file_name(self, temp_path: Path, file_path: Path) -> str:
        return str(file_path).replace(str(temp_path), '')


ZIP_UP_SINGLETON = ZipUp()
