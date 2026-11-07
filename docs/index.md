# jamstack

A small static site generator built on **Python** and **Jinja**. You write
Markdown and templates, run one command, and deploy the generated folder
anywhere.

!!! warning "2.0 is under development"

    This documentation describes the 2.0 engine. It is not published on PyPI
    yet; install it from the `2.0` branch as shown below. The `stable` branch
    holds the current 1.x release.

## Install

```bash
python -m pip install "jamstack @ git+https://github.com/jamstackpy/jamstack@2.0"
```

Python 3.11 or newer. Once 2.0 is released, `pip install jamstack` is enough.

## Quick start

```bash
jamstack init my-site --theme blog
cd my-site
jamstack build
jamstack serve
```

Your site is generated in `dist/` and served at `http://127.0.0.1:8000/`.
Edit anything under `content/` and the page rebuilds on the next save.

## What you get

- **Markdown or Jinja pages.** Write posts in Markdown with TOML front matter,
  or drop an `.html` file when you want full control of the markup.
- **Themes as folders.** Two ship with the package; a project can override
  either one, or add its own.
- **A real development loop.** The server rebuilds on change, debounces rapid
  saves, and keeps the last good build when a template fails.
- **The boring essentials.** `sitemap.xml`, an Atom feed, clean URLs, and a
  themed `404.html`, generated from the same sources.
- **No hidden machinery.** Three runtime dependencies, deterministic output,
  and no network access during a build.

## Where to go next

| Page | What it covers |
| --- | --- |
| [Tutorial](tutorial.md) | Build a blog from an empty folder in a few minutes. |
| [Content](content.md) | Front matter, URL rules, drafts, and HTML pages. |
| [Configuration](configuration.md) | Every key in `site.toml`. |
| [Themes](themes.md) | The theme format and the template API. |
| [Command line](cli.md) | Commands, options, and exit codes. |
| [Deployment](deployment.md) | GitHub Pages, Netlify, and Cloudflare Pages. |
| [Migration from 1.x](migration.md) | Convert a `settings.py`/`static.py` project. |
