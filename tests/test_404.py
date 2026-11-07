from pathlib import Path

import pytest

from jamstack.builder import build
from jamstack.config import load_config
from jamstack.theme import discover_themes

BUNDLED_THEMES = [theme.name for theme in discover_themes(Path("/nonexistent"))]


@pytest.mark.parametrize("theme_name", BUNDLED_THEMES)
def test_every_bundled_theme_renders_a_404_page(tmp_path: Path, theme_name: str) -> None:
    (tmp_path / "content").mkdir()
    (tmp_path / "site.toml").write_text(
        f'[site]\ntitle = "Test Site"\n\n[theme]\nname = "{theme_name}"\n', encoding="utf-8"
    )
    (tmp_path / "content" / "index.md").write_text('+++\ntitle = "Home"\n+++\n', encoding="utf-8")

    build(load_config(tmp_path))

    not_found = (tmp_path / "dist" / "404.html").read_text(encoding="utf-8")
    assert "Page not found" in not_found
    assert "Test Site" in not_found
