import threading
import urllib.request
from pathlib import Path

from jamstack.builder import build
from jamstack.config import load_config
from jamstack.server import create_server


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
