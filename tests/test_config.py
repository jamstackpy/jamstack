from pathlib import Path

import pytest

from jamstack.config import ConfigError, load_config


def write_config(root: Path, text: str) -> None:
    (root / "site.toml").write_text(text, encoding="utf-8")


def test_loads_defaults(tmp_path: Path) -> None:
    write_config(tmp_path, '[site]\ntitle = "My Site"\n')

    config = load_config(tmp_path)

    assert config.title == "My Site"
    assert config.output == tmp_path / "dist"
    assert config.theme == "minimal"
    assert config.language == "en"


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        load_config(tmp_path)


def test_requires_title(tmp_path: Path) -> None:
    write_config(tmp_path, "[site]\n")

    with pytest.raises(ConfigError, match="title"):
        load_config(tmp_path)


def test_rejects_invalid_theme_name(tmp_path: Path) -> None:
    write_config(tmp_path, '[site]\ntitle = "x"\n\n[theme]\nname = "../evil"\n')

    with pytest.raises(ConfigError, match="invalid theme"):
        load_config(tmp_path)


def test_custom_output(tmp_path: Path) -> None:
    write_config(tmp_path, '[site]\ntitle = "x"\n\n[build]\noutput = "public"\n')

    assert load_config(tmp_path).output == tmp_path / "public"
