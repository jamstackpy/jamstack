from datetime import date
from pathlib import Path

import pytest

from jamstack.content import ContentError, load_pages


def write_page(root: Path, name: str, text: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_parses_front_matter_and_url(tmp_path: Path) -> None:
    write_page(tmp_path, "about.md", '+++\ntitle = "About"\ndate = 2026-01-02\n+++\n\nHello\n')

    [page] = load_pages(tmp_path)

    assert page.title == "About"
    assert page.date == date(2026, 1, 2)
    assert page.url == "/about/"
    assert page.output.as_posix() == "about/index.html"
    assert page.template == "page.html"


def test_index_page_uses_root_url_and_index_template(tmp_path: Path) -> None:
    write_page(tmp_path, "index.md", '+++\ntitle = "Home"\n+++\n')

    [page] = load_pages(tmp_path)

    assert page.url == "/"
    assert page.output.as_posix() == "index.html"
    assert page.template == "index.html"


def test_nested_pages_and_drafts(tmp_path: Path) -> None:
    write_page(tmp_path, "blog/index.md", '+++\ntitle = "Blog"\n+++\n')
    write_page(tmp_path, "blog/draft.md", '+++\ntitle = "Draft"\ndraft = true\n+++\n')

    assert [page.title for page in load_pages(tmp_path)] == ["Blog"]
    assert [page.title for page in load_pages(tmp_path, drafts=True)] == ["Blog", "Draft"]


def test_default_title_from_filename(tmp_path: Path) -> None:
    write_page(tmp_path, "my-page.md", "Body\n")

    [page] = load_pages(tmp_path)

    assert page.title == "My Page"


def test_unterminated_front_matter(tmp_path: Path) -> None:
    write_page(tmp_path, "broken.md", '+++\ntitle = "x"\n')

    with pytest.raises(ContentError, match="unterminated"):
        load_pages(tmp_path)


def test_duplicate_output_detected(tmp_path: Path) -> None:
    write_page(tmp_path, "about.md", '+++\ntitle = "A"\n+++\n')
    write_page(tmp_path, "about/index.md", '+++\ntitle = "B"\n+++\n')

    with pytest.raises(ContentError, match="both build to"):
        load_pages(tmp_path)


def test_invalid_date_rejected(tmp_path: Path) -> None:
    write_page(tmp_path, "post.md", '+++\ntitle = "P"\ndate = "not-a-date"\n+++\n')

    with pytest.raises(ContentError, match="invalid date"):
        load_pages(tmp_path)
