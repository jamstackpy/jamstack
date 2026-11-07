import os
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from jamstack.builder import build
from jamstack.config import load_config
from jamstack.server import create_server, snapshot, watch


def make_site(root: Path) -> None:
    (root / "content").mkdir()
    (root / "site.toml").write_text('[site]\ntitle = "Served Site"\n', encoding="utf-8")
    (root / "content" / "index.md").write_text(
        '+++\ntitle = "Home"\n+++\n\nHello server\n', encoding="utf-8"
    )


def test_create_server_serves_the_build_output(tmp_path: Path) -> None:
    make_site(tmp_path)
    config = load_config(tmp_path)
    build(config)

    server = create_server(config, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as response:
            body = response.read().decode("utf-8")
        assert response.status == 200
        assert "Hello server" in body
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_server_serves_the_generated_404_page(tmp_path: Path) -> None:
    make_site(tmp_path)
    config = load_config(tmp_path)
    build(config)

    server = create_server(config, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with pytest.raises(urllib.error.HTTPError) as excinfo:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/missing/", timeout=5)
        assert excinfo.value.code == 404
        assert "Page not found" in excinfo.value.read().decode("utf-8")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_snapshot_detects_new_and_modified_files(tmp_path: Path) -> None:
    existing = tmp_path / "a.txt"
    existing.write_text("a", encoding="utf-8")

    first = snapshot([tmp_path, tmp_path / "missing"])
    assert str(existing) in first

    os.utime(existing, ns=(1_000_000_000, 2_000_000_000))
    assert snapshot([tmp_path])[str(existing)] == (2_000_000_000, 1)

    added = tmp_path / "b.txt"
    added.write_text("b", encoding="utf-8")
    assert str(added) in snapshot([tmp_path])


def test_watch_rebuilds_when_content_changes(tmp_path: Path) -> None:
    make_site(tmp_path)
    config = load_config(tmp_path)
    build(config)

    stop = threading.Event()
    watcher = threading.Thread(target=watch, args=(config, False, 0.05, stop), daemon=True)
    watcher.start()
    try:
        time.sleep(0.2)
        (tmp_path / "content" / "index.md").write_text(
            '+++\ntitle = "Home"\n+++\n\nFresh body\n', encoding="utf-8"
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if "Fresh body" in (tmp_path / "dist" / "index.html").read_text(encoding="utf-8"):
                break
            time.sleep(0.05)
        assert "Fresh body" in (tmp_path / "dist" / "index.html").read_text(encoding="utf-8")
    finally:
        stop.set()
        watcher.join(timeout=5)


def test_watch_survives_a_broken_template(tmp_path: Path) -> None:
    make_site(tmp_path)
    config = load_config(tmp_path)
    build(config)

    stop = threading.Event()
    watcher = threading.Thread(target=watch, args=(config, False, 0.05, stop), daemon=True)
    watcher.start()
    try:
        time.sleep(0.2)
        templates = tmp_path / "templates"
        templates.mkdir()
        (templates / "index.html").write_text("{{ missing_variable }}", encoding="utf-8")
        time.sleep(0.4)

        (templates / "index.html").unlink()
        (tmp_path / "content" / "index.md").write_text(
            '+++\ntitle = "Home"\n+++\n\nRecovered body\n', encoding="utf-8"
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if "Recovered body" in (tmp_path / "dist" / "index.html").read_text(encoding="utf-8"):
                break
            time.sleep(0.05)
        assert "Recovered body" in (tmp_path / "dist" / "index.html").read_text(encoding="utf-8")
        assert watcher.is_alive()
    finally:
        stop.set()
        watcher.join(timeout=5)
