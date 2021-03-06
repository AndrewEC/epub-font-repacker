import os
from typing import Generator, List
from pathlib import Path
from zipfile import ZipFile, ZIP_STORED

from repack.progress_printer import Printer


_MIMETYPE_FILE = 'mimetype'
_REPACKED_EPUB_NAME_TEMPLATE = '{} - Repacked.epub'


def _get_files_to_archive(temp_path: Path) -> List[Path]:
    def yield_all_files_in_path(path_to_traverse: Path) -> Generator[Path, None, None]:
        for file in os.listdir(path_to_traverse):
            file_path = path_to_traverse.joinpath(file)
            if file_path.is_file():
                yield file_path
            else:
                yield from yield_all_files_in_path(file_path)
    return list(yield_all_files_in_path(temp_path))


def _get_sorted_list_of_files_to_archive(temp_path: Path) -> List[Path]:
    files_to_archive = _get_files_to_archive(temp_path)
    # The epub 3 specification stipulates that the mimetype file should be the first entry in the zip file
    # To adhere to this rule we first have to find the manifest file and move to the front of the list of the files to
    # archive
    index_of_mimetype_file = next((index_and_filename[0] for index_and_filename in enumerate(files_to_archive) if str(index_and_filename[1]).endswith(_MIMETYPE_FILE)))
    mime_type_file = files_to_archive.pop(index_of_mimetype_file)
    files_to_archive.insert(0, mime_type_file)
    return files_to_archive


def _determine_archive_name(temp_path: Path, file_path: Path) -> str:
    return str(file_path).replace(str(temp_path), '')


def create_epub_zip(epub_path: Path, temp_path: Path):
    """
    This will zip up all the files located under the temp_path into a single epub file and place the epub file at
    the location specified by the epub_path.

    This will also ensure that the mimetype file is the first entry in the epub zip.

    :param epub_path: The absolute path of the epub file that will be generated after this method has been executed.
    :param temp_path: The path to the files that will be added to the epub file.
    """
    repacked_name = _REPACKED_EPUB_NAME_TEMPLATE.format(epub_path.stem)
    repacked_path = epub_path.parent.joinpath(repacked_name)

    files_to_archive = _get_sorted_list_of_files_to_archive(temp_path)

    print(f'Zipping [{len(files_to_archive)}] files into repacked epub')
    with Printer(len(files_to_archive)) as printer:
        with ZipFile(repacked_path, 'w', ZIP_STORED) as zippy:
            for file in files_to_archive:
                with printer.progress_tick(f'Zipping: [{file.stem}]'):
                    zippy.write(file, _determine_archive_name(temp_path, file))

    print(f'Repacked epub generated to: [{repacked_path}]')
