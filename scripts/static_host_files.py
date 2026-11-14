"""Write host-neutral headers and a real missing-page document for static builds."""
from pathlib import Path


HEADERS = '''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Cache-Control: no-cache

/browser-engine.mjs
  Content-Type: application/javascript; charset=utf-8

/browser-worker.mjs
  Content-Type: application/javascript; charset=utf-8

/models/*
  Content-Type: application/octet-stream

/package-parts/*
  Content-Type: application/octet-stream
'''


def write_static_host_files(destination: Path, source: Path) -> None:
    """Do not label stored gzip model bytes as an HTTP content encoding."""
    (destination / '_headers').write_text(HEADERS, encoding='utf-8')
    (destination / '404.html').write_bytes((source / '404.html').read_bytes())
