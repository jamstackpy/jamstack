from datetime import UTC, date, datetime, time
from pathlib import Path
from xml.etree import ElementTree

from jamstack.config import Config
from jamstack.content import Page

ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


def write_sitemap(config: Config, pages: list[Page], output: Path) -> Path | None:
    if not config.base_url or not pages:
        return None

    root = ElementTree.Element("urlset", xmlns=SITEMAP_NAMESPACE)
    for page in pages:
        url = ElementTree.SubElement(root, "url")
        ElementTree.SubElement(url, "loc").text = absolute_url(config, page.url)
        if page.date:
            ElementTree.SubElement(url, "lastmod").text = page.date.isoformat()

    return _write(root, output / "sitemap.xml")


def write_feed(config: Config, pages: list[Page], output: Path) -> Path | None:
    entries = [page for page in pages if page.date is not None]
    if not config.base_url or not entries:
        return None

    site_url = absolute_url(config, "/")
    root = ElementTree.Element("feed", xmlns=ATOM_NAMESPACE, lang=config.language)
    ElementTree.SubElement(root, "title").text = config.title
    if config.description:
        ElementTree.SubElement(root, "subtitle").text = config.description
    ElementTree.SubElement(root, "link", href=site_url, rel="alternate")
    ElementTree.SubElement(root, "link", href=absolute_url(config, "/feed.xml"), rel="self")
    ElementTree.SubElement(root, "id").text = site_url
    ElementTree.SubElement(root, "updated").text = _timestamp(
        max(page.date for page in entries if page.date)
    )
    author = ElementTree.SubElement(root, "author")
    ElementTree.SubElement(author, "name").text = config.author or config.title

    for page in entries:
        url = absolute_url(config, page.url)
        entry = ElementTree.SubElement(root, "entry")
        ElementTree.SubElement(entry, "title").text = page.title
        ElementTree.SubElement(entry, "link", href=url)
        ElementTree.SubElement(entry, "id").text = url
        ElementTree.SubElement(entry, "updated").text = _timestamp(page.date)
        summary = str(page.meta.get("summary", "")).strip()
        if summary:
            ElementTree.SubElement(entry, "summary").text = summary
        content = ElementTree.SubElement(entry, "content", type="html")
        content.text = str(page.content)

    return _write(root, output / "feed.xml")


def absolute_url(config: Config, path: str) -> str:
    return config.base_url.rstrip("/") + path


def _timestamp(value: date) -> str:
    return datetime.combine(value, time.min, tzinfo=UTC).isoformat()


def _write(root: ElementTree.Element, destination: Path) -> Path:
    ElementTree.indent(root, space="  ")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(
        ElementTree.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    )
    return destination
