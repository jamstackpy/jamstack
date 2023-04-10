import os
from pathlib import Path

import click

from jamstack.api.file import trycopytree

package_folder = Path(__file__).parent.absolute()
sites_path = os.path.join(package_folder, 'sites')


@click.group(help="Jamstack command line interface")
def cli():
    pass


@click.command(help="Create an empty, plain repository")
@click.argument('project_name')
@click.option('--existing/--not-existing', default=False)
def plain(project_name, existing):
    path = '.'

    trycopytree(
        os.path.join(sites_path, 'plain'),
        os.path.join(path, project_name),
        existing
    )


@click.command(help="Create a repository from a template")
@click.argument('template')
@click.argument('project_name')
@click.option('--existing/--not-existing', default=False)
def t(template, project_name, existing):
    path = '.'
    namespace, project = template.split('/')

    trycopytree(
        os.path.join(sites_path, namespace, project),
        os.path.join(path, project_name),
        existing
    )


cli.add_command(plain)
cli.add_command(t)


def main():
    cli()


if __name__ == "__main__":
    cli()
