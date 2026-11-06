from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


def create_environment(template_dirs: list[Path]) -> Environment:
    return Environment(
        loader=FileSystemLoader([str(path) for path in template_dirs]),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
