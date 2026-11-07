# Contributing

The project is developed on the `2.0` branch. Bug reports and pull requests go
to [github.com/jamstackpy/jamstack](https://github.com/jamstackpy/jamstack).

## Local setup

```bash
git clone git@github.com:jamstackpy/jamstack.git
cd jamstack
git switch 2.0
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

## Checks

```bash
ruff check .
ruff format --check .
pytest
```

The same checks run in CI on Python 3.11 through 3.14. A pull request that
changes behaviour needs a test that would fail without the change.

## Commits

Commits follow [Conventional Commits](https://www.conventionalcommits.org/) in
English:

```
feat(cli): add a --drafts flag to build
fix(content): reject dates without a year
docs: explain local theme overrides
```

One commit is one reviewable intention. Put mechanical changes (renames,
formatting, dependency bumps) in their own commit, and do not leave
intermediate commits that fail the tests. When the change needs context, add
a bullet-point body explaining what and why.

`commitizen` validates the message through the `commit-msg` hook.

## Pull requests

- Target `2.0`.
- Keep user-facing text and documentation in English.
- Do not rewrite pushed history.

The full guide, including the release process, lives in
[CONTRIBUTING.md](https://github.com/jamstackpy/jamstack/blob/2.0/CONTRIBUTING.md).
