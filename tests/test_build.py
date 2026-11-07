from pathlib import Path

import pytest

from jamstack.builder import build
from jamstack.config import load_config
from jamstack.theme import discover_themes

BUNDLED_THEMES = [theme.name for theme in discover_themes(Path("/nonexistent"))]


def make_site(root: Path, theme: str = "minimal") -> None:
    (root / "content").mkdir()
    (root / "static").mkdir()
    (root / "site.toml").write_text(
        f'[site]\ntitle = "Test Site"\n\n[theme]\nname = "{theme}"\n', encoding="utf-8"
    )
    (root / "content" / "index.md").write_text(
        '+++\ntitle = "Home"\n+++\n\nWelcome\n', encoding="utf-8"
    )
    (root / "content" / "about.md").write_text(
        '+++\ntitle = "About"\n+++\n\nAbout **us**\n', encoding="utf-8"
    )
    (root / "static" / "extra.txt").write_text("extra", encoding="utf-8")


def test_build_renders_pages_and_copies_static(tmp_path: Path) -> None:
    make_site(tmp_path)

    result = build(load_config(tmp_path))

    assert result.page_count == 2
    index = (tmp_path / "dist" / "index.html").read_text(encoding="utf-8")
    about = (tmp_path / "dist" / "about" / "index.html").read_text(encoding="utf-8")
    assert "Test Site" in index
    assert "<strong>us</strong>" in about
    assert (tmp_path / "dist" / "style.css").is_file()
    assert (tmp_path / "dist" / "extra.txt").read_text(encoding="utf-8") == "extra"


def test_project_templates_override_theme(tmp_path: Path) -> None:
    make_site(tmp_path)
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "page.html").write_text("OVERRIDE {{ page.title }}", encoding="utf-8")

    build(load_config(tmp_path))

    rendered = (tmp_path / "dist" / "about" / "index.html").read_text(encoding="utf-8")
    assert rendered == "OVERRIDE About"


def test_html_page_is_rendered_as_template(tmp_path: Path) -> None:
    make_site(tmp_path)
    (tmp_path / "content" / "raw.html").write_text(
        '+++\ntitle = "Raw"\n+++\n<p>{{ site.title }}</p>', encoding="utf-8"
    )

    build(load_config(tmp_path))

    rendered = (tmp_path / "dist" / "raw" / "index.html").read_text(encoding="utf-8")
    assert "<p>Test Site</p>" in rendered


def test_clean_removes_stale_files(tmp_path: Path) -> None:
    make_site(tmp_path)
    stale = tmp_path / "dist" / "stale.txt"
    stale.parent.mkdir(parents=True)
    stale.write_text("old", encoding="utf-8")

    build(load_config(tmp_path), clean=True)

    assert not stale.exists()


def test_drafts_are_excluded_by_default(tmp_path: Path) -> None:
    make_site(tmp_path)
    (tmp_path / "content" / "draft.md").write_text(
        '+++\ntitle = "Draft"\ndraft = true\n+++\n', encoding="utf-8"
    )

    build(load_config(tmp_path))
    assert not (tmp_path / "dist" / "draft").exists()

    build(load_config(tmp_path), drafts=True)
    assert (tmp_path / "dist" / "draft" / "index.html").is_file()


@pytest.mark.parametrize("theme_name", BUNDLED_THEMES)
def test_every_bundled_theme_builds(tmp_path: Path, theme_name: str) -> None:
    make_site(tmp_path, theme=theme_name)

    result = build(load_config(tmp_path))

    assert result.page_count == 2
    assert (tmp_path / "dist" / "index.html").is_file()
    assert (tmp_path / "dist" / "about" / "index.html").is_file()


def test_blog_theme_lists_only_dated_posts(tmp_path: Path) -> None:
    make_site(tmp_path, theme="blog")
    (tmp_path / "content" / "post.md").write_text(
        '+++\ntitle = "First Post"\ndate = 2026-01-02\ntemplate = "post"\n'
        'summary = "A summary"\n+++\n\nBody text\n',
        encoding="utf-8",
    )

    build(load_config(tmp_path))

    index = (tmp_path / "dist" / "index.html").read_text(encoding="utf-8")
    assert "First Post" in index
    assert 'href="/post/"' in index
    assert "A summary" in index
    assert "About" not in index
    assert (tmp_path / "dist" / "post" / "index.html").is_file()
