"""Audit the local official UNSW-NB15 train/test files."""

from __future__ import annotations

import argparse
from pathlib import Path

from nids_benchmark.data import build_data_manifest, load_official_splits, write_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--output", type=Path, default=Path("artifacts/data/data_manifest.json")
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bundle = load_official_splits(args.raw_dir)
    manifest = build_data_manifest(bundle)
    write_manifest(manifest, args.output)
    train = manifest["files"]["train"]["audit"]
    test = manifest["files"]["test"]["audit"]
    print(f"PASS train={train['rows']}x{train['columns']} test={test['rows']}x{test['columns']}")
    print(f"Manifest: {args.output}")


if __name__ == "__main__":
    main()
