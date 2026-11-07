import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

THEME_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class JamstackError(Exception):
    """Base class for expected, user-facing failures."""


class ConfigError(JamstackError):
    """Raised when site.toml is missing or invalid."""


@dataclass(frozen=True)
class Config:
    root: Path
    title: str
    description: str
    author: str
    base_url: str
    language: str
    output: Path
    theme: str


def load_config(root: Path) -> Config:
    path = root / "site.toml"
    if not path.is_file():
        raise ConfigError(f"{path} not found. Run 'jamstack init' first.")

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"{path}: {error}") from error

    site = data.get("site", {})
    build = data.get("build", {})
    theme = data.get("theme", {})

    title = str(site.get("title", "")).strip()
    if not title:
        raise ConfigError(f"{path}: [site].title is required")

    theme_name = str(theme.get("name", "minimal"))
    if not THEME_NAME_PATTERN.fullmatch(theme_name):
        raise ConfigError(f"{path}: invalid theme name {theme_name!r}")

    return Config(
        root=root,
        title=title,
        description=str(site.get("description", "")),
        author=str(site.get("author", "")),
        base_url=str(site.get("base_url", "")),
        language=str(site.get("language", "en")),
        output=root / str(build.get("output", "dist")),
        theme=theme_name,
    )
