+++
title = "Installation"
section = "getting-started"
order = 2
+++

Install the package and create a site:

```bash
pip install jamstack
jamstack init my-docs --theme minimal
cd my-docs
jamstack build
```

To try this example exactly as it is:

```bash
jamstack build examples/handbook
jamstack serve examples/handbook --port 8000
```

The second command rebuilds when a file changes. It is the same engine, only
the theme and the content differ.
