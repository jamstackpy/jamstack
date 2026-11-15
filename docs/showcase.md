# Showcase

Four sites built with the same engine. Each one lives under
[`examples/`](https://github.com/jamstackpy/jamstack/tree/stable/examples) and
is compiled in CI, so these screenshots match what the code produces.

## Minimal

[![The minimal theme: a single centred column with a title and one paragraph](assets/showcase/minimal.png)](https://github.com/jamstackpy/jamstack/tree/stable/examples/minimal)

The smallest possible site: one Markdown page and the bundled `minimal` theme.
A good starting point for a landing page.

## Blog

[![The blog theme: a centred masthead followed by dated posts with summaries](assets/showcase/blog.png)](https://github.com/jamstackpy/jamstack/tree/stable/examples/blog)

Dated posts, a feed and a sitemap. Shows the `blog` theme and how `date` and
`summary` shape the index.

## Atlas

[![The atlas theme: a local theme with a navigation bar, a hero and a grid of guides](assets/showcase/atlas.png)](https://github.com/jamstackpy/jamstack/tree/stable/examples/atlas)

A local theme copied into the project: nested routes, a guide index, reading
time computed in Jinja, template and static overrides, and a themed 404.

## Handbook

[![The handbook theme: a documentation layout with a sidebar and previous and next links](assets/showcase/handbook.png)](https://github.com/jamstackpy/jamstack/tree/stable/examples/handbook)

A documentation layout with a sidebar built from front matter (`section`,
`order`), a configurable section order through `[extra.sidebar]`,
previous/next links and footer content from `[extra]`.
