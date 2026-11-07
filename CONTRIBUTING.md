# Contributing

## Development setup

```bash
git clone git@github.com:jamstackpy/jamstack.git
cd jamstack
git switch stable
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

Run the checks before opening a pull request:

```bash
ruff check .
ruff format --check .
pytest
```

## Commits

Commits follow [Conventional Commits](https://www.conventionalcommits.org/) in
English:

```
feat(cli): add a --drafts flag to build
fix(content): reject dates without a year
docs: explain local theme overrides
```

One commit is one reviewable intention. Do not mix unrelated changes under a
message that only describes one of them, and do not leave intermediate commits
that fail the tests. Mechanical changes (renames, formatting, dependency
bumps) go in their own commit.

Write a body when the change needs context: bullet points, in English,
explaining what and why. `commitizen` validates the message through the
`commit-msg` hook installed above.

## Pull requests

- Target the `stable` branch.
- Include a test for new behaviour; bug fixes should include the case that
  reproduces the bug.
- Keep user-facing strings and documentation in English.
- Do not rewrite pushed history.

## Versioning

The project follows Semantic Versioning. The full policy, including what counts as a breaking change and how deprecations work, lives in [docs/versioning.md](docs/versioning.md).

## Releasing

Publishing runs on tags through GitHub Actions and PyPI trusted publishing,
with no API tokens stored anywhere.

One-time setup:

1. On PyPI, open the `jamstack` project → Publishing → add a GitHub publisher
   with owner `jamstackpy`, repository `jamstack`, workflow `release.yml`, and
   environment `pypi`.
2. On GitHub, create an environment named `pypi` in the repository settings.

Releases use `cz bump`. It updates `src/jamstack/__about__.py`, rewrites
`CHANGELOG.md`, commits the result, and creates the tag in one step:

```bash
cz bump --increment patch   # or minor, major
git push origin stable
git push origin v<version>
```

The `Release` workflow runs on tags matching `v*` and fails if the tag does not
match `src/jamstack/__about__.py`. Pre-releases work the same way with
`cz bump --prerelease rc`.

Review the generated section before pushing the tag. It is a draft: keep only
user-visible changes, list breaking changes first, and fix the wording.

The `Release` workflow also creates the GitHub release from that same section,
so the changelog is the single source of truth for the notes. Pre-release tags
are published as GitHub pre-releases.
