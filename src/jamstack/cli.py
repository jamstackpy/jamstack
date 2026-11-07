import json
import shutil
from pathlib import Path

import click

from jamstack.__about__ import __version__
from jamstack.builder import build as build_site
from jamstack.config import JamstackError, load_config
from jamstack.server import serve as serve_site
from jamstack.theme import discover_themes, resolve_theme

INDEX_PAGE = """+++
title = "Welcome"
+++

This is your new site. Edit `content/index.md` and run `jamstack build`.
"""


@click.group()
@click.version_option(__version__, prog_name="jamstack")
def main() -> None:
    """Static site generator built on Python and Jinja."""


@main.command()
@click.argument("path", default=".", type=click.Path(path_type=Path))
@click.option(
    "--theme", default="minimal", show_default=True, help="Theme to scaffold the site with."
)
@click.option("--force", is_flag=True, help="Write into a non-empty directory.")
def init(path: Path, theme: str, force: bool) -> None:
    """Create a new site."""
    if path.is_file():
        raise click.ClickException(f"{path} is a file, not a directory")

    if path.is_dir() and any(path.iterdir()) and not force:
        raise click.ClickException(f"{path} is not empty. Use --force to write anyway.")

    selected = resolve_theme(theme, path)

    site_toml = f"""[site]
title = {json.dumps(path.resolve().name.replace("-", " ").replace("_", " ").title())}
description = ""
base_url = ""
language = "en"

[build]
output = "dist"

[theme]
name = {json.dumps(theme)}
"""

    if selected.scaffold:
        shutil.copytree(selected.scaffold, path, dirs_exist_ok=True)

    files = {
        "site.toml": site_toml,
        "content/index.md": INDEX_PAGE,
        ".gitignore": "dist/\n",
    }
    for relative, content in files.items():
        destination = path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    click.echo(f"Created site in {path} using the {theme!r} theme")
    click.echo("Next steps:")
    click.echo(f"  cd {path}")
    click.echo("  jamstack build")


@main.command()
@click.option("--clean", is_flag=True, help="Delete the output directory before building.")
@click.option("--drafts", is_flag=True, help="Include pages marked as drafts.")
def build(clean: bool, drafts: bool) -> None:
    """Build the site into the output directory."""
    try:
        config = load_config(Path.cwd())
        result = build_site(config, clean=clean, drafts=drafts)
    except JamstackError as error:
        raise click.ClickException(str(error)) from error

    click.echo(f"Built {result.page_count} page(s) into {result.output}")


@main.command()
@click.option("--port", default=8000, show_default=True, type=click.IntRange(0, 65535))
@click.option("--drafts", is_flag=True, help="Include pages marked as drafts.")
def serve(port: int, drafts: bool) -> None:
    """Build the site, serve it, and rebuild on changes."""
    try:
        config = load_config(Path.cwd())
        serve_site(config, port=port, drafts=drafts)
    except JamstackError as error:
        raise click.ClickException(str(error)) from error


@main.command("themes")
def list_themes() -> None:
    """List the available themes."""
    try:
        themes = discover_themes(Path.cwd())
    except JamstackError as error:
        raise click.ClickException(str(error)) from error

    width = max(len(theme.name) for theme in themes)
    for theme in themes:
        origin = "bundled" if theme.bundled else "local"
        click.echo(f"{theme.name:<{width}}  {origin:<7}  {theme.description}")
