# Changelog

All notable changes to this project are documented in this file.

## 2.1.1 (2026-11-07)

### Bug fixes

- Publish the package under the Apache-2.0 license it has always used. The
  metadata for 2.0.0 and 2.1.0 incorrectly declared MIT.

## 2.1.0 (2026-11-07)

### Features

- Render Markdown tables in `.md` pages.
- Override a page URL with the `url` front matter key. Invalid values now fail
  the build instead of being silently ignored.

### Bug fixes

- Serve the generated `404.html` with a 404 status from `jamstack serve`.

## 2.0.0 (2026-11-07)

### Breaking

- The engine was rewritten. Projects built with `settings.py`, `static.py` or
  the html5up themes must migrate to `site.toml` and `content/`; see
  [the migration guide](docs/migration.md).
- Python 3.11 or newer is required.
- The html5up themes are no longer bundled or downloaded. 2.0 ships its own
  `minimal` and `blog` themes.

### Features

- `jamstack init` creates a site from a bundled theme.
- `site.toml` configures the title, description, author, base URL, output
  directory and theme.
- Markdown and Jinja pages in `content/` use TOML front matter and map to clean
  URLs.
- `jamstack build` renders every page through Jinja with strict undefined
  handling and copies the theme and project static files.
- Themes are discovered from the bundled set and from `themes/` in the project;
  templates and static files can be overridden per project.
- `jamstack themes` lists the available themes and their origin.
- `jamstack serve` serves the output over HTTP and rebuilds when a source
  changes.
- `sitemap.xml` and an Atom `feed.xml` are generated when `base_url` is set,
  and themes can provide a `404.html`.

### Bug fixes

- `serve` keeps watching after a failed rebuild.
- `serve` flushes status messages when output is redirected.

## 1.1.0

* Bulk refactors and code documentation
* New commands for `static.py` files
    * `--serve` for livewatch changes
    * `--watch` for watch specific files and folders.
    * `--port` especiffy serve port

## 1.0.0

* Back to namespace method for write templates names
    * Example: `html5up/massively` instead of just `massively`
* Template assets are not included in the library to minimize the size of the library, they were moved to
  a [separate repository](https://github.com/jamstackpy/jamstack-templates).

## 0.1.0

* Improve **Plain** template
* Add new templates (massively, phantom)
* When creating a project, instead of writing the template like this: **html5up/massively**, you can use the name
  directly, i.e. **massively**
* The assets of each template are now included in the library

## 0.0.4

* Add README.md info

## 0.0.3

* Add plain template

## 0.0.1

* Initial release
