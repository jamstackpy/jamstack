# Configuration

`site.toml` lives at the project root and is the only configuration file. It
must exist before `jamstack build`; `jamstack init` creates it.

```toml
[site]
title = "My Site"
description = "Notes on small tools."
author = "Your Name"
base_url = "https://example.com"
language = "en"

[build]
output = "dist"

[theme]
name = "blog"
```

## `[site]`

| Key | Required | Default | Used for |
| --- | --- | --- | --- |
| `title` | yes | — | Site name in templates, feed title, generated `site.toml`. |
| `description` | no | `""` | Meta description in themes, feed subtitle. |
| `author` | no | `""` | Feed author. Falls back to `title` when empty. |
| `base_url` | no | `""` | Absolute URL for `sitemap.xml` and `feed.xml`. |
| `language` | no | `"en"` | `lang` attribute in themes. |

`title` is trimmed and cannot be empty; the build stops with
`[site].title is required` if it is.

### `base_url`

Set it to the public URL of the deployed site, including the scheme and
without a trailing slash:

```toml
base_url = "https://example.com"
```

When it is set, the build writes `sitemap.xml` with every page and `feed.xml`
with every dated page. When it is empty, both files are skipped: emitting a
sitemap with relative URLs is invalid, and silently inventing a domain is
worse.

If the site is published under a subpath, include it:
`https://example.com/blog`.

## `[build]`

| Key | Default | Meaning |
| --- | --- | --- |
| `output` | `"dist"` | Directory where the generated site is written, relative to the project root. |

The output directory is replaced file by file on each build. Use
`jamstack build --clean` to delete it first, which removes files left over
from pages you deleted.

## `[theme]`

| Key | Default | Meaning |
| --- | --- | --- |
| `name` | `"minimal"` | Theme to render with. |

The name must match `^[a-z0-9][a-z0-9_-]*$`. Jamstack resolves it from
`<project>/themes/<name>/` first and falls back to the themes bundled with the
package. See [Themes](themes.md).

## Behaviour worth knowing

- Unknown keys are ignored, so a future version can add options without
  breaking old files.
- Relative paths are resolved from the project root, not from the current
  directory; commands must be run inside the project.
- `jamstack serve` watches `site.toml`, so editing it triggers a rebuild like
  any content change.
- The file is parsed with `tomllib`; invalid TOML stops the build and reports
  the file and line.
