import tomllib
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt
from markupsafe import Markup

from jamstack.config import JamstackError

FRONT_MATTER_DELIMITER = "+++"
MARKDOWN = MarkdownIt("commonmark", {"html": True})


class ContentError(JamstackError):
    """Raised when a content file cannot be parsed."""


@dataclass
class Page:
    source: Path
    url: str
    output: Path
    title: str
    template: str
    date: date | None
    draft: bool
    body: str
    meta: dict[str, Any] = field(default_factory=dict)
    content: Markup = field(default_factory=Markup)


def load_pages(content_dir: Path, *, drafts: bool = False) -> list[Page]:
    if not content_dir.is_dir():
        return []

    sources = sorted(
        path
        for path in content_dir.rglob("*")
        if path.is_file() and path.suffix in {".md", ".html"}
    )

    pages: list[Page] = []
    seen_outputs: dict[Path, Path] = {}
    for source in sources:
        page = load_page(source, content_dir)
        if page.draft and not drafts:
            continue
        if page.output in seen_outputs:
            raise ContentError(
                f"{source} and {seen_outputs[page.output]} both build to {page.output}"
            )
        seen_outputs[page.output] = source
        pages.append(page)

    pages.sort(key=lambda page: page.title.lower())
    pages.sort(key=lambda page: page.date or date.min, reverse=True)
    return pages


def load_page(source: Path, content_dir: Path) -> Page:
    text = source.read_text(encoding="utf-8")
    meta, body = split_front_matter(text, source)

    relative = source.relative_to(content_dir).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "index":
        parts.pop()

    return Page(
        source=source,
        url="/" + "".join(f"{part}/" for part in parts) if parts else "/",
        output=Path(*parts, "index.html"),
        title=parse_title(meta, relative.name),
        template=parse_template(meta, relative.name),
        date=parse_date(meta.get("date"), source),
        draft=bool(meta.get("draft", False)),
        body=body,
        meta=meta,
    )


def split_front_matter(text: str, source: Path) -> tuple[dict[str, Any], str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != FRONT_MATTER_DELIMITER:
        return {}, text

    for index in range(1, len(lines)):
        if lines[index].strip() != FRONT_MATTER_DELIMITER:
            continue

        raw = "".join(lines[1:index])
        body = "".join(lines[index + 1 :]).lstrip("\n")
        try:
            return tomllib.loads(raw), body
        except tomllib.TOMLDecodeError as error:
            raise ContentError(f"{source}: invalid front matter: {error}") from error

    raise ContentError(f"{source}: unterminated front matter")


def parse_title(meta: dict[str, Any], stem: str) -> str:
    title = str(meta.get("title", "")).strip()
    return title or stem.replace("-", " ").replace("_", " ").title()


def parse_template(meta: dict[str, Any], stem: str) -> str:
    template = str(meta.get("template", "")).strip()
    return template or ("index" if stem == "index" else "page")


def parse_date(value: Any, source: Path) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as error:
            raise ContentError(f"{source}: invalid date {value!r}") from error
    raise ContentError(f"{source}: date must be an ISO date, got {value!r}")


def render_markdown(body: str) -> Markup:
    return Markup(MARKDOWN.render(body))
