# Command line

```
jamstack [OPTIONS] COMMAND [ARGS]
```

Run `jamstack --help` or `jamstack <command> --help` for the same reference in
the terminal. `python -m jamstack` behaves identically.

## `jamstack init`

Create a new site.

```bash
jamstack init [PATH] [--theme NAME] [--force]
```

| Option | Default | Meaning |
| --- | --- | --- |
| `PATH` | `.` | Directory to create the site in. |
| `--theme NAME` | `minimal` | Theme to scaffold with. Use `jamstack themes` to list them. |
| `--force` | off | Write into a non-empty directory. |

It creates `site.toml`, `content/index.md`, and a `.gitignore` with `dist/`
plus any files the theme ships in its `scaffold/` directory. It refuses to
write into a file, or into a non-empty directory without `--force`.

```bash
jamstack init my-blog --theme blog
```

## `jamstack build`

Build the site into the configured output directory.

```bash
jamstack build [--clean] [--drafts]
```

| Option | Meaning |
| --- | --- |
| `--clean` | Delete the output directory before building. |
| `--drafts` | Include pages with `draft = true`. |

Reports how many pages were built. Use `--clean` when you have deleted or
renamed pages and want their old output gone.

## `jamstack serve`

Build, serve the output, and rebuild when sources change.

```bash
jamstack serve [--port PORT] [--drafts]
```

| Option | Default | Meaning |
| --- | --- | --- |
| `--port PORT` | `8000` | Port to bind on `127.0.0.1`. `0` picks any free port. |
| `--drafts` | off | Include drafts. |

The server watches `site.toml`, `content/`, `templates/`, `static/`, and the
active theme's directories. Changes are debounced: a burst of saves produces
one rebuild. If a rebuild fails, the error is printed and the previous build
keeps being served.

Stop it with `Ctrl+C`.

## `jamstack themes`

List the themes available to the current project, marking each as `bundled`
or `local`, with the description from its manifest.

```bash
jamstack themes
```

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Success. |
| `1` | A user-facing error: missing `site.toml`, invalid content, template failure, port in use. |
| `2` | Invalid usage: unknown command or option. |

Errors go to standard error, so `jamstack build` can be used in scripts and CI
without parsing output.
