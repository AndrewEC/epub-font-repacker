import click

from buildutils import BuildConfiguration
from buildutils.plugins import (
    FlakePlugin,
    GenericCommandPlugin,
    EnsureVenvActivePlugin
)


@click.command()
@click.option('--profile', '-pr')
@click.option('--plugins', '-p')
@click.option('--list-plugins', '-l', is_flag=True)
def main(profile: str, plugins: str, list_plugins: bool):
    (
        BuildConfiguration()
        .config('build.ini')
        .plugins(
            EnsureVenvActivePlugin(),
            GenericCommandPlugin('INSTALL', 'Install required dependencies from requirements.txt file.'),
            FlakePlugin(),
            GenericCommandPlugin('AUDIT', 'Audit the dependencies in the requirements.txt file for vulnerabilities.')
        )
        .build(profile, plugins, list_plugins)
    )


if __name__ == '__main__':
    main()
