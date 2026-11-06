import shutil
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment
from markupsafe import Markup

from jamstack.config import Config
from jamstack.content import Page, load_pages, render_markdown
from jamstack.render import create_environment
from jamstack.theme import resolve_theme


@dataclass(frozen=True)
class BuildResult:
    output: Path
    page_count: int


def build(config: Config, *, clean: bool = False, drafts: bool = False) -> BuildResult:
    theme = resolve_theme(config.theme, config.root)

    template_dirs = [path for path in (config.root / "templates", theme.templates) if path.is_dir()]
    environment = create_environment(template_dirs)

    pages = load_pages(config.root / "content", drafts=drafts)

    if clean and config.output.exists():
        shutil.rmtree(config.output)
    config.output.mkdir(parents=True, exist_ok=True)

    for page in pages:
        context = {"site": config, "page": page, "pages": pages}
        page.content = render_page_body(environment, page, context)
        html = environment.get_template(page.template).render(context)
        destination = config.output / page.output
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding="utf-8")

    copy_static(theme.static, config.output)
    copy_static(config.root / "static", config.output)

    return BuildResult(output=config.output, page_count=len(pages))


def render_page_body(environment: Environment, page: Page, context: dict[str, object]) -> Markup:
    if page.source.suffix == ".html":
        return Markup(environment.from_string(page.body).render(context))
    return render_markdown(page.body)


def copy_static(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
