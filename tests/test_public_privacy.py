"""A rebuild must remove stale private files and leave original handoffs intact."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts.build_public_presentation import build


ROOT = Path(__file__).resolve().parents[1]


class PublicPrivacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / 'demo/presentation'
        shutil.copytree(ROOT / 'demo/presentation', source,
                        ignore=shutil.ignore_patterns('assets'))
        (source / 'assets').mkdir()
        for name in ('AP_MEAN_STD.csv', 'OPERATING_POINTS_MEAN_STD.csv'):
            shutil.copy2(ROOT / 'demo/presentation/assets' / name, source / 'assets' / name)
        (source / 'assets/BAO_CAO_DOT3.pdf').write_bytes(b'PRIVATE_DOCUMENT_SENTINEL')
        shutil.copytree(ROOT / 'demo/cases', self.root / 'demo/cases')
        (self.root / 'demo/cases/private-notes.md').write_text('not a CSV demo')
        config = self.root / 'deployment/cloudflare'
        config.mkdir(parents=True)
        shutil.copy2(ROOT / 'deployment/cloudflare/private-documents.json', config)
        self.policy = json.loads((config / 'private-documents.json').read_text())
        self.dist = self.root / 'sites/nids-presentation/dist'
        (self.dist / 'models').mkdir(parents=True)
        (self.dist / 'models/demo.bin.gz').write_bytes(b'\x1f\x8bunchanged model')
        (self.dist / 'models/manifest.json').write_text(json.dumps({
            'models': [{'file': 'demo.bin.gz'}],
        }))

    def test_rebuild_prunes_private_bytes_and_uses_restricted_links(self):
        private = ('assets/BAO_CAO_DOT3.pdf', 'downloads/report.pdf',
                   'downloads/source.zip', 'downloads/study.md',
                   'downloads/MANIFEST.json', 'package-parts/old.part',
                   'ho-so.js', 'models/private-notes.txt', 'forgotten.txt')
        for name in private:
            path = self.dist / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'PRIVATE_DOCUMENT_SENTINEL')
        report_source = self.root / 'demo/presentation/assets/BAO_CAO_DOT3.pdf'
        original = report_source.read_bytes()
        local_hub = (self.root / 'demo/presentation/ho-so.html').read_bytes()
        model = (self.dist / 'models/demo.bin.gz').read_bytes()
        build(self.root)
        for name in private:
            self.assertFalse((self.dist / name).exists(), name)
        self.assertEqual(report_source.read_bytes(), original)
        self.assertEqual((self.root / 'demo/presentation/ho-so.html').read_bytes(), local_hub)
        self.assertEqual((self.dist / 'models/demo.bin.gz').read_bytes(), model)
        self.assertFalse((self.dist / 'cases/private-notes.md').exists())
        self.assertTrue((self.dist / 'cases/normal.csv').is_file())
        self.assertTrue((self.dist / 'browser-worker.mjs').is_file())
        index = (self.dist / 'index.html').read_text(encoding='utf-8')
        hub = (self.dist / 'ho-so.html').read_text(encoding='utf-8')
        self.assertIn(self.policy['round3_url'], index)
        self.assertIn(self.policy['reports_url'], hub)
        self.assertIn(self.policy['root_url'], hub)
        self.assertNotIn('#page=', index)
        self.assertNotIn('feedback-form', hub)
        self.assertNotIn('practice-dialog', hub)
        self.assertNotIn('{{', hub)
        for path in self.dist.rglob('*'):
            if path.is_file() and path.suffix != '.gz':
                self.assertNotIn(b'PRIVATE_DOCUMENT_SENTINEL', path.read_bytes(), str(path))
        # A repeated build must not reintroduce documents from the source directory.
        before = {p.relative_to(self.dist).as_posix(): p.read_bytes()
                  for p in self.dist.rglob('*') if p.is_file()}
        build(self.root)
        after = {p.relative_to(self.dist).as_posix(): p.read_bytes()
                 for p in self.dist.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_catalog_cannot_publish_paths_outside_csv_cases(self):
        path = self.root / 'demo/cases/catalog.json'
        catalog = json.loads(path.read_text(encoding='utf-8'))
        for name in ('../private.csv', 'private.pdf'):
            catalog['cases'][0]['filename'] = name
            path.write_text(json.dumps(catalog), encoding='utf-8')
            with self.assertRaises(ValueError):
                build(self.root)

    def test_public_archive_attachment_is_retired_without_changing_files(self):
        missing = self.root / 'never-read.zip'
        before = (ROOT / 'deployment/cloudflare/download-manifest.json').read_bytes()
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/attach_cloudflare_download.py'),
                                 str(missing)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Public ZIP attachment was retired', result.stderr)
        self.assertEqual((ROOT / 'deployment/cloudflare/download-manifest.json').read_bytes(), before)
        self.assertFalse(missing.exists())


if __name__ == '__main__':
    unittest.main()
