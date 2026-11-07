# Migrating from 1.x to 2.0

2.0 is a rewrite of the engine, not an update. The 1.x model — a copy of
`static.py` and `settings.py` inside every project, themes downloaded from
GitHub, Flask declared as a dependency — is gone. Projects built with 1.x do
not run on 2.0 without conversion, and there is no automated converter.

This guide walks through the conversion. Keep the 1.x site running with
`python -m pip install "jamstack<2"` until the new build looks right.

## What changed

| 1.x | 2.0 |
| --- | --- |
| `jamstack plain <name>` | `jamstack init <name>` |
| `jamstack t html5up/massively <name>` | `jamstack init <name> --theme blog` (or your own theme) |
| `settings.py` with `OUTPUT_FOLDER` | `site.toml` with `[build] output` |
| `posts.json` | one Markdown file per post with front matter |
| `python static.py` | `jamstack build` |
| `python static.py --serve` | `jamstack serve` |
| `--watch` and `--port` flags | watch is automatic; `--port` still exists |
| `--jamdo` asset downloader | removed; themes ship their own assets |
| html5up themes | removed from the package |
| Jinja context with `info` and `posts` | `site`, `page`, `pages` |
| Python 3.6+ | Python 3.11+ |

Flask is no longer a dependency. It was declared in 1.x but never imported by
the code.

## Step 1: create a 2.0 project

Do not convert in place. Create a parallel project and copy into it:

```bash
jamstack init new-site --theme minimal
```

Use `--theme blog` if the site is a dated blog. Both themes are documented in
[themes.md](themes.md).

## Step 2: convert `settings.py`

1.x projects carry a `settings.py` that points at the output directory and
sometimes at JSON data. Everything configurable now lives in `site.toml`:

```toml
[site]
title = "My Site"
description = "What the site is about"
base_url = "https://example.com"

[build]
output = "dist"

[theme]
name = "minimal"
```

Set `base_url` only when you know the public URL; it enables `sitemap.xml` and
`feed.xml`.

## Step 3: convert `posts.json`

In 1.x every post was an entry in `posts.json` that pointed at a template
file. In 2.0 each post is a file under `content/`:

```markdown
+++
title = "My first post"
date = 2026-11-06
summary = "A short description for listings and feeds."
+++

The body, in Markdown.
```

The path determines the URL: `content/posts/my-first-post.md` becomes
`/posts/my-first-post/`. Drafts get `draft = true` and are skipped unless you
build with `--drafts`.

## Step 4: bring your templates

If you used a bundled html5up theme, it no longer exists in 2.0. You have two
options:

1. Redesign with the `minimal` or `blog` theme and move content into their
   structure.
2. Keep your 1.x templates by turning them into a local theme:

```
new-site/
  themes/
    legacy/
      theme.toml
      templates/
        index.html
        page.html
        ...
      static/
        assets/
```

`theme.toml`:

```toml
name = "legacy"
description = "Templates imported from my 1.x site."
```

Then set `[theme] name = "legacy"` in `site.toml`. Templates that extended
`base.html` keep working as long as you adjust the variables:

- `page.title`, `page.content`, `page.date`, `page.meta` for the current page.
- `pages` for every page in the build, already sorted.
- `site.title`, `site.description`, `site.language` for global values.

The Jinja environment is now strict: a missing variable fails the build
instead of rendering an empty string. That is intentional — it catches typos
that 1.x silently ignored.

## Step 5: move assets to `static/`

Anything the templates load by path — CSS, images, fonts — belongs in
`static/`. Its contents are copied to the root of `dist/`, so
`static/assets/site.css` is served at `/assets/site.css`. Project files
overwrite the theme's files with the same path.

## Step 6: build and compare

```bash
jamstack build
jamstack serve --port 8000
```

Check the URL map: 1.x wrote one HTML file per source template, while 2.0
turns `content/about.md` into `dist/about/index.html` (clean URLs by default).
If your host expects `.html` paths, adjust the template links, not the engine.

## If you keep html5up templates

The html5up designs that shipped with 1.x are licensed CC BY 3.0, which
requires visible attribution. They are not part of the 2.0 package. If you
import them as a local theme, keep the original credits in the footer.

## Getting help

Open an issue with the 1.x `site.toml` equivalent, the template that fails,
and the full error output. The `stable` branch still contains the 1.x source
for reference.
