# Deployment

A build produces a folder of static files. There is nothing to run on the
server: upload `dist/` to any host that serves files, and that is the whole
deployment.

Three things to check before the final build:

1. `base_url` in `site.toml` is the real public URL.
2. The final build uses `--clean`, so deleted pages do not linger.
3. `dist/` is not committed (the generated `.gitignore` already excludes it).

```bash
jamstack build --clean
```

## GitHub Pages

The most direct setup is a workflow that builds on every push and publishes
with the official Pages actions. In the site repository, create
`.github/workflows/pages.yml`:

```yaml
name: Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install "jamstack @ git+https://github.com/jamstackpy/jamstack@2.0"
      - run: jamstack build --clean
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist
      - id: deployment
        uses: actions/deploy-pages@v4
```

Then set the repository's Pages source to **GitHub Actions**.

For a project site served under `https://user.github.io/repo/`, set
`base_url` to that full URL including the subpath, so the sitemap and feed
links resolve correctly.

If you publish by pushing a `gh-pages` branch instead, add an empty
`.nojekyll` file to `dist/` so GitHub Pages does not preprocess the output.

## Netlify

| Setting | Value |
| --- | --- |
| Build command | `pip install "jamstack @ git+https://github.com/jamstackpy/jamstack@2.0" && jamstack build --clean` |
| Publish directory | `dist` |

Netlify's build image must provide Python 3.11 or newer. If it does not,
build the site in your own CI and deploy the resulting `dist/` as a prebuilt
site.

## Cloudflare Pages

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | `pip install "jamstack @ git+https://github.com/jamstackpy/jamstack@2.0" && jamstack build --clean` |
| Build output directory | `dist` |

As with Netlify, if the build image lacks a suitable Python, build elsewhere
and upload `dist/` directly.

## Any other host

Copy the contents of `dist/` to the web root. Two details depend on the host:

- **Clean URLs.** The site writes `about/index.html`, which every common host
  serves at `/about/`. A host that only maps `/about/` to `/about.html` needs
  a rewrite rule, but this is rare.
- **404 pages.** `dist/404.html` is produced when the active theme provides a
  `404.html` template. GitHub Pages, Netlify, and Cloudflare Pages pick it up
  automatically; other hosts may need to be told the filename.

## Caching

Every build writes the same paths with new contents. If your host caches
aggressively, either purge the cache on deploy or give the HTML a short
`Cache-Control` and the assets a long one. Asset filenames are not hashed yet,
so immutable caching on `/style.css` will keep serving stale CSS after a
deploy.
