# Examples

Complete sites built with jamstack. Each directory is a standalone project with
its own `site.toml`, and CI builds every one of them on each change.

| Example | What it shows |
|---|---|
| [`minimal`](minimal/) | The smallest site: one page and the bundled `minimal` theme. |
| [`blog`](blog/) | Posts with dates and summaries using the bundled `blog` theme. |
| [`atlas`](atlas/) | A local theme with its own navigation, guides, nested routes, overrides and a draft. |
| [`handbook`](handbook/) | A documentation site: configurable sidebar, previous/next links and footer links from `[extra]`. |

## Running one

```bash
cd examples/handbook
jamstack build --clean
jamstack serve
```

To build all of them from the repository root:

```bash
for site in examples/*/; do (cd "$site" && jamstack build --clean); done
```
