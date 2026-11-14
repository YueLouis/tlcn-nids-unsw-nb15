"""Split a validated offline ZIP into static assets below the Cloudflare file limit."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    with zipfile.ZipFile(args.package) as archive:
        if archive.testzip() is not None:
            raise ValueError('Archive CRC failed')
    destination = root / 'sites/nids-presentation/dist/package-parts'
    destination.mkdir(parents=True, exist_ok=True)
    rows, digest = [], hashlib.sha256()
    with args.package.open('rb') as source:
        number = 0
        while data := source.read(20 * 1024 * 1024):
            digest.update(data)
            filename = f'ATTQ_NIDS_20261114_{number:02}.part'
            (destination / filename).write_bytes(data)
            rows.append(dict(path='/package-parts/' + filename, bytes=len(data),
                             sha256=hashlib.sha256(data).hexdigest()))
            number += 1
    manifest = dict(path='/downloads/ATTQ_NIDS_BAN_GIAO_20261114.zip',
                    filename='ATTQ_NIDS_BAN_GIAO_20261114.zip',
                    bytes=args.package.stat().st_size, sha256=digest.hexdigest(), parts=rows)
    (root / 'deployment/cloudflare/download-manifest.json').write_text(
        json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest))


if __name__ == '__main__':
    main()
