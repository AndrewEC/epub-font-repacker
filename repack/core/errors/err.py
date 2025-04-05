from pathlib import Path


class _InvalidEpubException(Exception):

    _MESSAGE_TEMPLATE = '{} \nThis likely means the epub file does not conform to the epub 3 specification.'

    def __init__(self, base_message: str):
        super().__init__(_InvalidEpubException._MESSAGE_TEMPLATE.format(base_message))


class EpubNotFoundException(Exception):

    _MESSAGE_TEMPLATE = 'Could not find epub file at location: [{}]'

    def __init__(self, location: Path):
        super().__init__(EpubNotFoundException._MESSAGE_TEMPLATE.format(location))


class OpfException(Exception):

    def __init__(self, base: Exception):
        super().__init__(f'Could not locate OPF file to update. Cause: [{base}]')


class MissingOpfException(_InvalidEpubException):

    _MESSAGE_TEMPLATE = ('The opf file specified in the container.xml definition could not '
                         'be found at the specified location: [{}]')

    def __init__(self, expected_location: Path):
        super().__init__(MissingOpfException._MESSAGE_TEMPLATE.format(expected_location))


class MissingMimetypeFileException(_InvalidEpubException):

    def __init__(self):
        super().__init__('Could not repackage epub file because the mimetype file could not be found.')


class MissingContainerFileException(_InvalidEpubException):

    _MESSAGE_TEMPLATE = 'The container.xml file could not be found at the expected location of: [{}].'

    def __init__(self, expected_location: Path):
        super().__init__(MissingContainerFileException._MESSAGE_TEMPLATE.format(expected_location))


class ParseException(_InvalidEpubException):

    _MESSAGE_TEMPLATE = 'The container.xml file could not be parsed as xml. Cause: [{}]'

    def __init__(self, exception: Exception):
        super().__init__(ParseException._MESSAGE_TEMPLATE.format(exception))


class PathAlreadyExistsException(Exception):

    _MESSAGE_TEMPLATE = ('A path could not be created because it already exists. '
                         'Please delete the following path and try again: [{}]')

    def __init__(self, temp_path: Path):
        super().__init__(PathAlreadyExistsException._MESSAGE_TEMPLATE.format(temp_path))


class MissingResourceException(Exception):

    _MESSAGE_TEMPLATE = ('A required resource could not be found at [{}].'
                         '\nThis could mean the resource has been deleted/moved or '
                         'was not successfully downloaded from Github.')

    def __init__(self, resource: Path):
        super().__init__(MissingResourceException._MESSAGE_TEMPLATE.format(resource))
