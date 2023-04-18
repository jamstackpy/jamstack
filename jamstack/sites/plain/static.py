import argparse
from os.path import join

from livereload import Server

import settings
from jamstack.api.template import generate


def generate_site():
    extra_context = {"info": settings.info}
    generate('index.html', join(settings.OUTPUT_FOLDER, 'index.html'), context=extra_context)


def serve_files(port, watch):
    server = Server()
    for x in watch.split('|'):
        server.watch(x, func=generate_site)
    try:
        server.serve(root=settings.OUTPUT_FOLDER, port=port)
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Project manager.')
    parser.add_argument('--serve', action='store_true', help='Serve files for livewatch')
    parser.add_argument('--watch', type=str, default='*.py|templates|templates/sections', help='Files/Folders to watch')
    parser.add_argument('--port', type=int, default=8000, help='Port to serve')
    args = parser.parse_args()

    if args.serve:
        serve_files(args.port, args.watch)
    else:
        generate_site()
