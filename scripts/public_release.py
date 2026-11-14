"""Select the current report set without changing historical release files."""
from pathlib import Path


def report_downloads(root: Path) -> dict[str, Path]:
    current = root / 'docs/releases/final_handoff_20261114/reports'
    if current.is_dir():
        files = [current / name for name in (
            'NhomTLCN_dot4_20261114.pdf', 'NhomTLCN_tong_20261114.pdf',
            'Nguon_dot4_20261114.zip', 'Nguon_tong_20261114.zip')]
        for path in files:
            if not path.is_file():
                raise FileNotFoundError(f'Current release is incomplete: {path}')
    else:
        files = list((root / 'docs/releases/review_final_20261113/reports').iterdir())
    files += list((root / 'docs/releases/review_final_20261113/slides').iterdir())
    return {path.name: path for path in files
            if path.is_file() and path.suffix in ('.pdf', '.zip')}
