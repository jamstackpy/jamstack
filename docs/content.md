# Content

Everything under `content/` becomes the site. The engine reads `.md` and
`.html` files recursively; any other file is ignored.

## Files and URLs

The path of a file determines its URL and its output file:

| Source | URL | Output |
| --- | --- | --- |
| `content/index.md` | `/` | `dist/index.html` |
| `content/about.md` | `/about/` | `dist/about/index.html` |
| `content/posts/hello.md` | `/posts/hello/` | `dist/posts/hello/index.html` |
| `content/posts/2026/index.md` | `/posts/2026/` | `dist/posts/2026/index.html` |

A file named `index` maps to its directory instead of a subdirectory, which is
what makes clean URLs work. Two sources that resolve to the same output fail
the build instead of overwriting each other silently.

## Front matter

Markdown and HTML pages can start with TOML front matter between `+++` lines:

```markdown
+++
title = "Why static sites"
date = 2026-11-07
summary = "No runtime, no database, no surprises."
template = "post"
+++

The body starts here.
```

Front matter is optional. Without it, the title is derived from the file name
(`second-post.md` becomes "Second Post") and the default template is used.

### Recognised keys

| Key | Type | Default | Meaning |
| --- | --- | --- | --- |
| `title` | string | File name | Page title. |
| `date` | ISO date | none | Publication date. Drives ordering and feeds. |
| `template` | string | `index` or `page` | Template file, with or without `.html`. |
| `draft` | boolean | `false` | Skipped unless the build uses `--drafts`. |
| `summary` | string | none | Short description used by the blog theme and the feed. |

Any other key is kept in `page.meta` and is available to templates, so a theme
can support `cover`, `tags`, or anything else without engine changes.

### Dates

`date` accepts a TOML date (`2026-11-07`), a TOML datetime, or an ISO string.
Only the calendar date is used; times are discarded. An invalid value fails
the build with the source file in the message.

### Drafts

A page with `draft = true` is loaded but excluded from the build. To preview
it locally:

```bash
jamstack build --drafts
jamstack serve --drafts
```

Be careful not to deploy a `dist/` built with `--drafts`: drafts are included
in the sitemap and the feed.

## Markdown

Markdown is parsed as CommonMark with raw HTML enabled, so inline HTML works:

```markdown
A paragraph with a <mark>highlight</mark>.

<div class="note">A block written in HTML.</div>
```

The rendered HTML is exposed to templates as `page.content`, already marked
safe. Do not add `|safe` to it.

## HTML pages

A `.html` file is rendered as a Jinja template instead of Markdown. It receives
the same variables as any other page (`site`, `page`, `pages`), which makes it
useful for landing pages with custom markup:

```html
+++
title = "Landing"
+++

<section class="hero">
  <h1>{{ site.title }}</h1>
  <p>{{ site.description }}</p>
</section>

<ul>
  {% for item in pages if item.url != "/" %}
    <li><a href="{{ item.url }}">{{ item.title }}</a></li>
  {% endfor %}
</ul>
```

## Page order

Templates receive `pages` sorted by date, newest first, then by title. Pages
without a date sort after dated pages. The `blog` theme filters that list to
dated pages, which is why an about page does not appear among the posts.

## Errors you will see

- `invalid front matter`: the TOML between `+++` lines does not parse.
- `unterminated front matter`: the opening `+++` has no closing line.
- `invalid date`: the value is not an ISO date.
- `both build to …`: two files resolve to the same output path.

All of them stop the build and name the source file. The development server
keeps serving the last successful build while you fix the file.
