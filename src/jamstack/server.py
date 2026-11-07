import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from jamstack.builder import build
from jamstack.config import Config


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def create_server(config: Config, port: int = 8000) -> ThreadingHTTPServer:
    handler = functools.partial(_QuietHandler, directory=str(config.output.resolve()))
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


def serve(config: Config, port: int = 8000, drafts: bool = False) -> None:
    result = build(config, drafts=drafts)
    print(f"Built {result.page_count} page(s) into {result.output}")

    server = create_server(config, port)
    address, actual_port = server.server_address[:2]
    print(f"Serving at http://{address}:{actual_port}/ (Ctrl+C to stop)")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
