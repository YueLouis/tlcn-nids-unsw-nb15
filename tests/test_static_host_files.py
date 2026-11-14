"""Build metadata must preserve binary model bytes and allow current module loading."""
from pathlib import Path
import tempfile
import unittest

from scripts.static_host_files import write_static_host_files


class StaticHostFileTests(unittest.TestCase):
    def test_generated_headers_and_missing_page_do_not_modify_assets(self):
        source=Path(__file__).resolve().parents[1]/'demo/presentation'
        with tempfile.TemporaryDirectory() as directory:
            destination=Path(directory)
            (destination/'models').mkdir()
            model=destination/'models/test.bin.gz'
            original=b'\x1f\x8b\x08stored-model-bytes'
            model.write_bytes(original)
            write_static_host_files(destination,source)
            headers=(destination/'_headers').read_text(encoding='utf-8')
            blocks={}
            for block in headers.strip().split('\n\n'):
                lines=block.splitlines()
                blocks[lines[0]]={name.strip().lower():value.strip() for line in lines[1:] for name,_,value in [line.strip().partition(':')]}
            self.assertEqual(blocks['/*']['cache-control'],'no-cache')
            self.assertEqual(blocks['/*']['x-content-type-options'],'nosniff')
            for path in ('/browser-engine.mjs','/browser-worker.mjs'):
                self.assertEqual(blocks[path]['content-type'],'application/javascript; charset=utf-8')
            self.assertEqual(blocks['/models/*']['content-type'],'application/octet-stream')
            self.assertNotIn('content-encoding',headers.lower())
            self.assertEqual(model.read_bytes(),original)
            page=(destination/'404.html').read_text(encoding='utf-8')
            self.assertEqual((destination/'404.html').read_bytes(),(source/'404.html').read_bytes())
            self.assertIn('<html lang="vi">',page)
            self.assertIn('Không tìm thấy trang này',page)
            self.assertIn('href="/"',page)
            self.assertIn('href="/ho-so.html"',page)
            self.assertNotIn('<script',page)


if __name__=='__main__':
    unittest.main()
