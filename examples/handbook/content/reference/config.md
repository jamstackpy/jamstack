+++
title = "Configuration"
section = "reference"
order = 1
+++

`site.toml` has three fixed tables and one free-form table.

| Table | Purpose |
| --- | --- |
| `[site]` | Title, description, author, base URL and language |
| `[build]` | Output directory |
| `[theme]` | Theme name |
| `[extra]` | Anything the theme needs |

`[extra]` is not interpreted by the engine. This site reads footer text and
links from it, but the engine only guarantees that it is a table and exposes it
as `site.extra`.
