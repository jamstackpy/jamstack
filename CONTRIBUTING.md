# Contributing

## Development setup

```bash
git clone git@github.com:jamstackpy/jamstack.git
cd jamstack
git switch 2.0
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

- Target the `2.0` branch.
- Include a test for new behaviour; bug fixes should include the case that
  reproduces the bug.
- Keep user-facing strings and documentation in English.
- Do not rewrite pushed history.

## Releasing

Publishing runs on tags through GitHub Actions and PyPI trusted publishing,
with no API tokens stored anywhere.

One-time setup:

1. On PyPI, open the `jamstack` project → Publishing → add a GitHub publisher
   with owner `jamstackpy`, repository `jamstack`, workflow `release.yml`, and
   environment `pypi`.
2. On GitHub, create an environment named `pypi` in the repository settings.

For the first 2.0 release, the version in `src/jamstack/__about__.py` is
`2.0.0.dev0`. Set it to `2.0.0`, regenerate the changelog, and tag:

```bash
cz changelog
git commit -am "chore(release): 2.0.0"
git tag v2.0.0
git push origin 2.0 v2.0.0
```

Later releases use `cz bump`, which updates the version, rewrites
`CHANGELOG.md`, commits, and creates the tag in one step.
