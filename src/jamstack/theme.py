import tomllib
from dataclasses import dataclass
from pathlib import Path

from jamstack.config import JamstackError

PACKAGED_THEMES = Path(__file__).parent / "themes"


class ThemeError(JamstackError):
    """Raised when a theme cannot be resolved or is malformed."""


@dataclass(frozen=True)
class Theme:
    name: str
    description: str
    root: Path
    templates: Path
    static: Path
    scaffold: Path | None
    bundled: bool


def load_theme(root: Path, *, bundled: bool) -> Theme:
    manifest = root / "theme.toml"
    if not manifest.is_file():
        raise ThemeError(f"{root} is not a theme: theme.toml is missing")

    try:
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise ThemeError(f"{manifest}: {error}") from error

    name = str(data.get("name", "")).strip()
    if not name:
        raise ThemeError(f"{manifest}: name is required")
    if name != root.name:
        raise ThemeError(f"{manifest}: name {name!r} does not match directory {root.name!r}")

    templates = root / "templates"
    if not templates.is_dir():
        raise ThemeError(f"{manifest}: templates directory is missing")

    scaffold = root / "scaffold"
    return Theme(
        name=name,
        description=str(data.get("description", "")).strip(),
        root=root,
        templates=templates,
        static=root / "static",
        scaffold=scaffold if scaffold.is_dir() else None,
        bundled=bundled,
    )


def resolve_theme(name: str, project_root: Path) -> Theme:
    candidates = (
        (project_root / "themes" / name, False),
        (PACKAGED_THEMES / name, True),
    )
    for root, bundled in candidates:
        if root.is_dir():
            return load_theme(root, bundled=bundled)

    available = ", ".join(theme.name for theme in discover_themes(project_root))
    raise ThemeError(f"Theme {name!r} not found. Available themes: {available or 'none'}")


def discover_themes(project_root: Path) -> list[Theme]:
    themes: dict[str, Theme] = {}
    for root in sorted(PACKAGED_THEMES.iterdir()):
        if root.is_dir():
            theme = load_theme(root, bundled=True)
            themes[theme.name] = theme

    local_root = project_root / "themes"
    if local_root.is_dir():
        for root in sorted(local_root.iterdir()):
            if root.is_dir():
                theme = load_theme(root, bundled=False)
                themes[theme.name] = theme

    return sorted(themes.values(), key=lambda theme: theme.name)
