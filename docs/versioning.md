# Versioning policy

jamstack follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

## What counts as a breaking change

A major release is required when an existing site or theme stops working:

- Renaming or removing a CLI command, option or exit code.
- Removing or renaming a key in `site.toml`.
- Changing the front matter keys, or the URLs that `build` generates for pages.
- Changing the template context (`site`, `page`, `pages`) or the required fields of `theme.toml`.
- Raising the minimum Python version.

New commands, optional `site.toml` keys, new template variables and new bundled themes ship in a minor release. Bug fixes ship in a patch release; a patch never changes behaviour on purpose.

## Deprecations

A feature is deprecated before it is removed:

1. The changelog and the reference page mark it deprecated.
2. It keeps working for at least one minor release.
3. It is removed in the next major release.

When the engine can detect the old usage, the CLI prints a deprecation warning instead of failing silently.

## Supported versions

Only the latest major release receives fixes. `2.x` is the current line; `1.x` is unsupported. If a `3.0` is released, `2.x` will receive security fixes for six months after that release.

Python 3.11 or newer is required. Support for a Python version is dropped in a minor release once that version reaches end of life.

## Documentation versions

This site documents the latest release. The documentation for a specific version is available from its tag:

```text
https://github.com/jamstackpy/jamstack/tree/v2.0.0/docs
```
