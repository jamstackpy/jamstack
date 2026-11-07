# Changelog

All notable changes to this project are documented in this file. Entries before
2.0 were written by hand; later entries are generated from Conventional Commits.

## 2.0.0 (2026-11-07)

### Breaking

- The 1.x engine is gone: projects built with `settings.py`, `static.py` and the
  html5up themes must migrate to `site.toml` and `content/`. See `docs/migration.md`.

### Feat

- **themes**: render a 404 page from the active theme
- **feed**: generate sitemap.xml and an Atom feed
- **serve**: rebuild the site when sources change
- **serve**: serve the built site over HTTP
- **themes**: add theme manifests and a reading-first blog theme
- **build**: render sites with the bundled minimal theme
- **content**: parse front matter and resolve page URLs
- **config**: load and validate site.toml

### Fix

- **serve**: keep watching after a failed rebuild
- **serve**: flush status messages in redirected output

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
