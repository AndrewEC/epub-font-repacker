from pathlib import Path


class EpubNotFoundException(Exception):

    _MESSAGE_TEMPLATE = 'Could not find epub file at location: [{}]'

    def __init__(self, location: Path):
        super().__init__(EpubNotFoundException._MESSAGE_TEMPLATE.format(location))


class OpfLocationException(Exception):

    def __init__(self, base: Exception):
        super().__init__(f'Could not locate OPF file to update. Cause: [{base}]')


class MissingMimetypeFileException(Exception):

    def __init__(self):
        super().__init__('Could not repackage epub file because the mimetype file could not be found.')


class ParseException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
