# Theme specification

A theme is a directory. Jamstack resolves it from the project first and falls
back to the themes bundled with the package:

```
<project>/themes/<name>/     # wins if present
src/jamstack/themes/<name>/  # bundled with the package
```

`<name>` must match the `name` field in the manifest and the `[theme] name`
value in `site.toml`.

## Directory layout

```
mytheme/
  theme.toml        # required
  templates/        # required
  static/           # optional
  scaffold/         # optional
```

### `theme.toml`

```toml
name = "mytheme"
description = "A one-line description shown by 'jamstack themes'."
```

Both fields are strings. `name` is required and must equal the directory name;
`description` is optional.

### `templates/`

Jinja templates rendered with autoescaping enabled for `.html` and `.xml` and
with `StrictUndefined`, so referencing a missing variable fails the build
instead of rendering an empty string.

The engine picks the template for each page in this order:

1. The `template` key from the page's front matter.
2. `index.html` if the page is an `index` file, otherwise `page.html`.

The `template` value may omit the `.html` extension.

Templates receive three variables:

| Variable | Type | Contents |
| --- | --- | --- |
| `site` | config object | `title`, `description`, `author`, `base_url`, `language`, `output`, `theme`, `root` |
| `page` | page object | `title`, `url`, `date`, `draft`, `meta`, `content`, `source`, `output`, `template` |
| `pages` | list of pages | Every page in the build, sorted by date descending, then title ascending |

`page.content` is already rendered and marked safe: Markdown for `.md` files,
Jinja output for `.html` files. Wrap it in `{{ page.content }}` without a
`|safe` filter.

`page.meta` holds every front matter key, so themes can define their own
conventions (`summary`, `cover`, `tags`, …) without engine changes.

### `static/`

Copied recursively into the output root after the pages are written. If the
project also has a `static/` directory, the project's files are copied second
and overwrite the theme's, which is the supported way to replace a logo or a
stylesheet without forking the theme.

### `scaffold/`

Copied into the project only during `jamstack init`, before the generated
`site.toml` and starter content are written. Use it to ship example posts,
images, or a `content/` structure that makes sense for the theme. It is never
read during a build.

### `404.html` (optional)

If the theme provides `templates/404.html`, the engine renders it to
`dist/404.html` using `site` and `pages`. Static hosts such as GitHub Pages,
Netlify, and Cloudflare Pages serve that file automatically.

## Template overrides

The project's own `templates/` directory is searched before the theme's. To
tweak one file without copying the whole theme, create
`<project>/templates/page.html`; the rest keeps coming from the theme.

## Minimal theme

```
mytheme/
  theme.toml
  templates/
    base.html
    index.html
    page.html
  static/
    style.css
```

`theme.toml`

```toml
name = "mytheme"
description = "The smallest possible theme."
```

`templates/base.html`

```html
<!doctype html>
<html lang="{{ site.language }}">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}{{ site.title }}{% endblock %}</title>
    <link rel="stylesheet" href="/style.css">
  </head>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>
```

`templates/page.html`

```html
{% extends "base.html" %}

{% block title %}{{ page.title }} · {{ site.title }}{% endblock %}

{% block content %}
  <article>
    <h1>{{ page.title }}</h1>
    {{ page.content }}
  </article>
{% endblock %}
```

`templates/index.html`

```html
{% extends "base.html" %}

{% block content %}
  <h1>{{ page.title }}</h1>
  {{ page.content }}
  <ul>
    {% for item in pages if item.url != "/" %}
      <li><a href="{{ item.url }}">{{ item.title }}</a></li>
    {% endfor %}
  </ul>
{% endblock %}
```

Set `[theme] name = "mytheme"` in `site.toml` and run `jamstack build`.

## Rules the engine enforces

- A theme without `theme.toml` or `templates/` is rejected.
- The manifest name must match the directory name.
- A missing template, or an undefined variable in a template, fails the build
  with the offending file and line.
- A page whose output path collides with another page fails the build.
