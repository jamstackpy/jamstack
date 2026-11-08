+++
title = "Deploying"
section = "guides"
order = 3
+++

The build writes a self-contained directory, so any static host works.

1. Run `jamstack build --clean`.
2. Upload `dist/` to your host.
3. Point the domain at it.

Set `base_url` in `site.toml` to get an absolute `sitemap.xml` and `feed.xml`.
The `404.html` generated from the theme is used by hosts that support custom
error pages, and by `jamstack serve`.
