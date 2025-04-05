import click

from repack.core.processors import EPUB_PROCESSOR_SINGLETON


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
        EPUB_PROCESSOR_SINGLETON.process_epub_file(epub_file)
    except Exception as e:
        if stack:
            raise
        print(str(e))


if __name__ == '__main__':
    main()
