from pathlib import Path
import shutil

from repack.errors import PathAlreadyExistsException


class TempDirectory:

    """
    Enterable utility class to help create and delete a temp directory in which the contents of the epub
    file being modified can be extracted to so its contents can be further processes.

    This will throw an exception upon entry if the temp directory already exists.
    """

    def __init__(self, dir_path: Path):
        self._dir_path = dir_path
        if self._dir_path.is_dir():
            raise PathAlreadyExistsException(self._dir_path)

    def __enter__(self):
        self._dir_path.mkdir(exist_ok=False, parents=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._dir_path.is_dir():
                shutil.rmtree(self._dir_path)
        except Exception as e:
            print('The temp directory could not be deleted. It is safe to delete the following directory:')
            print(f'\t{self._dir_path}')
            print(f'The directory could not be deleted because: [{e}]')
