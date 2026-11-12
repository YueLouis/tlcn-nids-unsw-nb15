"""Serve a packaged browser demo on loopback using only the Python standard library."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent / 'web')
    parser.add_argument('--port', type=int, help='Use a specific port; otherwise try 4399 through 4409.')
    args = parser.parse_args()
    root = args.directory.resolve()
    if not (root / 'index.html').is_file():
        parser.error('Khong tim thay web/index.html. Hay giai nen day du goi offline.')
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    server = None
    ports = [args.port] if args.port is not None else range(4399, 4410)
    for port in ports:
        try:
            server = ThreadingHTTPServer(('127.0.0.1', port), handler)
            break
        except OSError:
            continue
    if server is None:
        parser.exit(1, 'Chua mo duoc cong local. Thu --port 4410 hoac dong ban demo cu roi chay lai.\n')
    print(f'Mo http://127.0.0.1:{server.server_port}/ trong trinh duyet; giu cua so nay mo. Ctrl+C de dung.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
