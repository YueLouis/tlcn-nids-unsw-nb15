"""Standalone download links must resolve outside the repository checkout."""
from pathlib import Path
import tempfile
import unittest

from scripts.portable_markdown import REPOSITORY, render_portable_markdown


class PortableMarkdownTests(unittest.TestCase):
    def test_files_directories_unicode_fragments_and_external_urls(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'docs').mkdir()
            (root/'src').mkdir()
            source=root/'docs/ghi chú.md'
            source.write_text('nội dung',encoding='utf-8')
            (root/'docs/bản tổng.pdf').write_bytes(b'pdf')
            text='\n'.join([
                '[PDF](<bản tổng.pdf> "Báo cáo")',
                '[Mã](../src/)',
                '[Mục](#mỗi-người)',
                '[Khác](ghi%20ch%C3%BA.md#c%C3%A1ch-%C4%91%E1%BB%8Dc)',
                '[Web](https://example.com/a?x=1#f)',
                '[Mail](mailto:test@example.com)',
                '[CDN](//example.com/a)',
            ])
            actual=render_portable_markdown(text,source,root)
            self.assertIn(f'[PDF](<{REPOSITORY}/blob/main/docs/b%E1%BA%A3n%20t%E1%BB%95ng.pdf> "Báo cáo")',actual)
            self.assertIn(f'[Mã]({REPOSITORY}/tree/main/src)',actual)
            self.assertIn(f'[Mục]({REPOSITORY}/blob/main/docs/ghi%20ch%C3%BA.md#m%E1%BB%97i-ng%C6%B0%E1%BB%9Di)',actual)
            self.assertIn('#c%C3%A1ch-%C4%91%E1%BB%8Dc)',actual)
            for link in text.splitlines()[-3:]:
                self.assertIn(link,actual)
            self.assertEqual(source.read_text(encoding='utf-8'),'nội dung')

    def test_rejects_missing_target_and_repository_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            source=root/'notes.md'
            source.write_text('',encoding='utf-8')
            for href in ('missing.md','../outside.md'):
                with self.subTest(href=href),self.assertRaises(ValueError):
                    render_portable_markdown(f'[link]({href})',source,root)


if __name__=='__main__':
    unittest.main()
