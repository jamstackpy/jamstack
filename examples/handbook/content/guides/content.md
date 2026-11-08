+++
title = "Writing content"
section = "guides"
order = 1
+++

Pages are Markdown or HTML. Front matter is TOML between `+++` lines:

```toml
+++
title = "Writing content"
section = "guides"
order = 1
+++
```

Keys the engine understands are `title`, `date`, `template`, `draft`, `summary`
and `url`. Everything else is kept as-is and is available to the theme as
`page.meta`, which is how this example reads `section`, `order` and
`nav_title`.
