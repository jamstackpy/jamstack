+++
title = "Introduction"
section = "getting-started"
order = 1
nav_title = "Introduction"
+++

This example is a documentation site: three sections, a persistent sidebar and
pages that are mostly prose.

The sidebar is built from front matter. Each page declares a `section` and an
`order`; the theme groups pages by section and sorts them by that number.

The section order comes from `site.toml`, not from the filesystem:

```toml
[extra.sidebar]
sections = ["getting-started", "guides", "reference"]
```

Any section missing from that list is appended alphabetically, so the site still
works if someone adds a page with a new section.
