from pathlib import Path

from click.testing import CliRunner

from jamstack.cli import main


def test_init_scaffolds_site(tmp_path: Path) -> None:
    result = CliRunner().invoke(main, ["init", str(tmp_path / "mysite")])

    assert result.exit_code == 0, result.output
    root = tmp_path / "mysite"
    assert (root / "site.toml").is_file()
    assert (root / "content" / "index.md").is_file()
    assert (root / ".gitignore").read_text(encoding="utf-8").strip() == "dist/"


def test_init_refuses_non_empty_directory(tmp_path: Path) -> None:
    (tmp_path / "existing.txt").write_text("x", encoding="utf-8")

    result = CliRunner().invoke(main, ["init", str(tmp_path)])

    assert result.exit_code != 0
    assert "not empty" in result.output


def test_init_force_overwrites(tmp_path: Path) -> None:
    (tmp_path / "existing.txt").write_text("x", encoding="utf-8")

    result = CliRunner().invoke(main, ["init", str(tmp_path), "--force"])

    assert result.exit_code == 0, result.output


def test_build_reports_missing_config(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(main, ["build"])

    assert result.exit_code != 0
    assert "site.toml" in result.output


def test_init_then_build(tmp_path: Path, monkeypatch) -> None:
    runner = CliRunner()
    assert runner.invoke(main, ["init", str(tmp_path / "site")]).exit_code == 0

    monkeypatch.chdir(tmp_path / "site")
    result = runner.invoke(main, ["build"])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "site" / "dist" / "index.html").is_file()
