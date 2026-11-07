from pathlib import Path
from xml.etree import ElementTree

from jamstack.builder import build
from jamstack.config import load_config
from jamstack.feed import ATOM_NAMESPACE, SITEMAP_NAMESPACE


def make_site(root: Path, *, theme: str = "minimal", base_url: str = "https://example.com") -> None:
    (root / "content").mkdir()
    (root / "site.toml").write_text(
        f'[site]\ntitle = "Test Site"\ndescription = "A test site"\n'
        f'author = "Ada"\nbase_url = "{base_url}"\n\n'
        f'[theme]\nname = "{theme}"\n',
        encoding="utf-8",
    )
    (root / "content" / "index.md").write_text(
        '+++\ntitle = "Home"\n+++\n\nWelcome\n', encoding="utf-8"
    )
    (root / "content" / "about.md").write_text(
        '+++\ntitle = "About"\n+++\n\nAbout **us**\n', encoding="utf-8"
    )


def test_sitemap_lists_every_page(tmp_path: Path) -> None:
    make_site(tmp_path)
    (tmp_path / "content" / "about.md").write_text(
        '+++\ntitle = "About"\ndate = 2026-01-02\n+++\n\nAbout\n', encoding="utf-8"
    )

    build(load_config(tmp_path))

    root = ElementTree.parse(tmp_path / "dist" / "sitemap.xml").getroot()
    locations = [element.text for element in root.iter(f"{{{SITEMAP_NAMESPACE}}}loc")]
    assert sorted(locations) == ["https://example.com/", "https://example.com/about/"]
    lastmods = [element.text for element in root.iter(f"{{{SITEMAP_NAMESPACE}}}lastmod")]
    assert lastmods == ["2026-01-02"]


def test_feed_lists_dated_pages_newest_first(tmp_path: Path) -> None:
    make_site(tmp_path, theme="blog")
    posts = tmp_path / "content" / "posts"
    posts.mkdir()
    (posts / "first.md").write_text(
        '+++\ntitle = "First"\ndate = 2026-01-02\ntemplate = "post"\n'
        'summary = "First summary"\n+++\n\nFirst **body**\n',
        encoding="utf-8",
    )
    (posts / "second.md").write_text(
        '+++\ntitle = "Second"\ndate = 2026-02-03\ntemplate = "post"\n+++\n\nSecond body\n',
        encoding="utf-8",
    )

    build(load_config(tmp_path))

    root = ElementTree.parse(tmp_path / "dist" / "feed.xml").getroot()
    entries = root.findall(f"{{{ATOM_NAMESPACE}}}entry")
    titles = [entry.findtext(f"{{{ATOM_NAMESPACE}}}title") for entry in entries]
    assert titles == ["Second", "First"]
    assert root.findtext(f"{{{ATOM_NAMESPACE}}}author/{{{ATOM_NAMESPACE}}}name") == "Ada"
    assert entries[1].findtext(f"{{{ATOM_NAMESPACE}}}summary") == "First summary"
    assert entries[0].findtext(f"{{{ATOM_NAMESPACE}}}id") == "https://example.com/posts/second/"
    assert "First <strong>body</strong>" in entries[1].findtext(f"{{{ATOM_NAMESPACE}}}content")


def test_generated_files_require_base_url(tmp_path: Path) -> None:
    make_site(tmp_path, base_url="")

    build(load_config(tmp_path))

    assert not (tmp_path / "dist" / "sitemap.xml").exists()
    assert not (tmp_path / "dist" / "feed.xml").exists()
