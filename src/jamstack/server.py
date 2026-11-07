import functools
import threading
from collections.abc import Iterable
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from jamstack.builder import build
from jamstack.config import Config
from jamstack.theme import resolve_theme


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def create_server(config: Config, port: int = 8000) -> ThreadingHTTPServer:
    handler = functools.partial(_QuietHandler, directory=str(config.output.resolve()))
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def watched_paths(config: Config) -> list[Path]:
    theme = resolve_theme(config.theme, config.root)
    return [
        config.root / "site.toml",
        config.root / "content",
        config.root / "templates",
        config.root / "static",
        theme.templates,
        theme.static,
    ]


def snapshot(paths: Iterable[Path]) -> dict[str, tuple[int, int]]:
    state: dict[str, tuple[int, int]] = {}
    for path in paths:
        if path.is_file():
            files: Iterable[Path] = [path]
        elif path.is_dir():
            files = path.rglob("*")
        else:
            continue
        for file in files:
            if file.is_file():
                stat = file.stat()
                state[str(file)] = (stat.st_mtime_ns, stat.st_size)
    return state


def watch(config: Config, drafts: bool, poll_interval: float, stop: threading.Event) -> None:
    paths = watched_paths(config)
    previous = snapshot(paths)
    while not stop.wait(poll_interval):
        current = snapshot(paths)
        if current == previous:
            continue
        stop.wait(poll_interval)  # let editors finish writing
        settled = snapshot(paths)
        if settled != current:
            continue
        previous = settled
        try:
            result = build(config, drafts=drafts)
        except Exception as error:  # a bad build must not kill the watcher
            print(f"Build failed: {error}", flush=True)
        else:
            print(f"Rebuilt {result.page_count} page(s)", flush=True)


def serve(
    config: Config, port: int = 8000, drafts: bool = False, poll_interval: float = 0.5
) -> None:
    result = build(config, drafts=drafts)
    print(f"Built {result.page_count} page(s) into {result.output}", flush=True)

    server = create_server(config, port)
    address, actual_port = server.server_address[:2]
    print(f"Serving at http://{address}:{actual_port}/ (Ctrl+C to stop)", flush=True)

    stop = threading.Event()
    watcher = threading.Thread(
        target=watch, args=(config, drafts, poll_interval, stop), daemon=True
    )
    watcher.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()
        watcher.join(timeout=5)
