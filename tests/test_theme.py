from pathlib import Path

import pytest

from jamstack.theme import ThemeError, discover_themes, resolve_theme


def write_theme(root: Path, name: str, description: str = "") -> Path:
    theme = root / "themes" / name
    (theme / "templates").mkdir(parents=True)
    (theme / "theme.toml").write_text(
        f'name = "{name}"\ndescription = "{description}"\n', encoding="utf-8"
    )
    return theme


def test_resolves_bundled_theme() -> None:
    theme = resolve_theme("minimal", Path("/nonexistent"))

    assert theme.bundled
    assert theme.templates.is_dir()


def test_local_theme_overrides_bundled(tmp_path: Path) -> None:
    write_theme(tmp_path, "minimal")

    theme = resolve_theme("minimal", tmp_path)

    assert not theme.bundled
    assert theme.root == tmp_path / "themes" / "minimal"


def test_missing_theme_lists_available(tmp_path: Path) -> None:
    with pytest.raises(ThemeError, match="blog"):
        resolve_theme("nope", tmp_path)


def test_theme_requires_manifest(tmp_path: Path) -> None:
    (tmp_path / "themes" / "broken" / "templates").mkdir(parents=True)

    with pytest.raises(ThemeError, match=r"theme\.toml"):
        resolve_theme("broken", tmp_path)


def test_theme_name_must_match_directory(tmp_path: Path) -> None:
    theme = write_theme(tmp_path, "local")
    (theme / "theme.toml").write_text('name = "other"\n', encoding="utf-8")

    with pytest.raises(ThemeError, match="does not match"):
        resolve_theme("local", tmp_path)


def test_discover_lists_bundled_and_local(tmp_path: Path) -> None:
    write_theme(tmp_path, "custom")

    names = [theme.name for theme in discover_themes(tmp_path)]

    assert names == ["blog", "custom", "minimal"]
