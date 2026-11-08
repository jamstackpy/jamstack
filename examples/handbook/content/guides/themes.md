+++
title = "Themes"
section = "guides"
order = 2
+++

A theme is a directory with a `theme.toml`, a `templates/` directory and an
optional `static/` directory.

The theme in this example lives in `themes/handbook`, so it is local to the
project. The engine looks there first and falls back to the bundled themes.

Templates in `templates/` at the project root override the theme ones. Static
files work the same way: the theme is copied first, then the project overwrites
what it needs.
