+++
title = "Command line"
section = "reference"
order = 2
+++

Four commands cover the whole workflow:

- `jamstack init PATH --theme NAME` creates a site.
- `jamstack build` renders `content/` into `dist/`.
- `jamstack serve` builds, serves and rebuilds on changes.
- `jamstack themes` lists bundled and local themes.

`build` accepts `--clean` to remove stale files and `--drafts` to include pages
marked `draft = true`.
