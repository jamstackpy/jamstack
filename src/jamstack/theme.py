from dataclasses import dataclass
from pathlib import Path

from jamstack.config import JamstackError

PACKAGED_THEMES = Path(__file__).parent / "themes"


class ThemeError(JamstackError):
    """Raised when the configured theme cannot be resolved."""


@dataclass(frozen=True)
class Theme:
    name: str
    root: Path
    templates: Path
    static: Path


def resolve_theme(name: str, project_root: Path) -> Theme:
    candidates = (project_root / "themes" / name, PACKAGED_THEMES / name)
    for root in candidates:
        if root.is_dir():
            break
    else:
        available = sorted(path.name for path in PACKAGED_THEMES.iterdir() if path.is_dir())
        raise ThemeError(
            f"Theme {name!r} not found. Available themes: {', '.join(available) or 'none'}"
        )

    templates = root / "templates"
    if not templates.is_dir():
        raise ThemeError(f"Theme {name!r} has no templates directory at {templates}")

    return Theme(name=name, root=root, templates=templates, static=root / "static")
