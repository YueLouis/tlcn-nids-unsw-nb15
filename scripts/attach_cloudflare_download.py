"""Retired: full offline packages are private Drive handoffs, never public assets."""
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.parse_args()
    parser.error('Public ZIP attachment was retired on 19/11/2026. '
                 'Keep reports, source ZIPs and the offline package in restricted Drive. '
                 'No files were read or changed.')


if __name__ == '__main__':
    main()
