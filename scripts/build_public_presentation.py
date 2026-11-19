"""Build the public demo; reports, source ZIPs and study documents stay in Drive."""
from pathlib import Path
import json
import shutil

try:
    from .static_host_files import write_static_host_files
except ImportError:
    from static_host_files import write_static_host_files


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = (
    'presentation.css', 'presentation.js', 'data.js', 'browser-engine.mjs',
    'browser-worker.mjs', 'browser-adapter.js', 'ho-so.css',
)
PUBLIC_CSVS = ('AP_MEAN_STD.csv', 'OPERATING_POINTS_MEAN_STD.csv')


def child_path(parent: Path, name: str) -> Path:
    """Allow only ordinary files immediately inside a known public directory."""
    if Path(name).name != name or '/' in name or '\\' in name or name in ('.', '..'):
        raise ValueError(f'Invalid public filename: {name}')
    path = parent / name
    if path.is_symlink() or path.resolve().parent != parent.resolve():
        raise ValueError(f'Public file escapes its directory: {path}')
    return path


def prune_public_files(destination: Path, allowed: set[str]) -> None:
    """Remove stale build files only inside the resolved, dedicated dist directory."""
    boundary = destination.resolve()
    files = list(destination.rglob('*'))
    for path in files:
        if path.is_symlink() or not path.resolve().is_relative_to(boundary):
            raise ValueError(f'Unexpected linked public asset: {path}')
    for path in files:
        if path.is_file() and path.relative_to(destination).as_posix() not in allowed:
            path.unlink()
    for path in sorted(files, key=lambda item: len(item.parts), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def build(root: Path = ROOT, destination: Path | None = None) -> Path:
    root = root.resolve()
    source = root / 'demo/presentation'
    destination = destination or root / 'sites/nids-presentation/dist'
    destination.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        raise ValueError('Public output cannot be a linked directory')
    destination = destination.resolve()
    policy = json.loads((root / 'deployment/cloudflare/private-documents.json').read_text(encoding='utf-8'))

    cases_source = root / 'demo/cases'
    catalog = json.loads((cases_source / 'catalog.json').read_text(encoding='utf-8'))
    case_names = {'catalog.json'}
    for case in catalog['cases']:
        name = case['filename']
        if not name.endswith('.csv'):
            raise ValueError(f'Only catalogued CSV cases may be public: {name}')
        child_path(cases_source, name)
        case_names.add(name)

    # Model export is a separate, verified step. Preserve only manifest-listed files.
    model_names = set()
    model_dir = destination / 'models'
    if (model_dir / 'manifest.json').is_file():
        manifest = json.loads((model_dir / 'manifest.json').read_text(encoding='utf-8'))
        model_names.add('manifest.json')
        for row in manifest['models']:
            name = row['file']
            if not name.endswith('.bin.gz'):
                raise ValueError(f'Invalid model export filename: {name}')
            child_path(model_dir, name)
            model_names.add(name)

    allowed = set(PUBLIC_FILES) | {'index.html', 'ho-so.html', 'SOURCE_DATA.json', '_headers', '404.html'}
    allowed.update('assets/' + name for name in PUBLIC_CSVS)
    allowed.update('cases/' + name for name in case_names)
    allowed.update('models/' + name for name in model_names)
    prune_public_files(destination, allowed)

    for name in PUBLIC_FILES:
        shutil.copy2(source / name, destination / name)
    (destination / 'assets').mkdir(exist_ok=True)
    for name in PUBLIC_CSVS:
        shutil.copy2(source / 'assets' / name, destination / 'assets' / name)
    (destination / 'cases').mkdir(exist_ok=True)
    for name in case_names:
        shutil.copy2(child_path(cases_source, name), destination / 'cases' / name)

    html = (source / 'index.html').read_text(encoding='utf-8')
    html = html.replace('<script src="presentation.js"></script>', '<script src="browser-adapter.js"></script>\n<script src="presentation.js"></script>')
    html = html.replace('<a href="/lab" class="small">Mở phòng thử nghiệm đầy đủ ↗</a>', '<span class="small muted browser-note">Bản online · CSV được xử lý trên trình duyệt</span>')
    html = html.replace('<a href="/lab">Mở phòng thử nghiệm đầy đủ ↗</a>', '<a href="https://github.com/YueLouis/tlcn-nids-unsw-nb15#readme" target="_blank" rel="noopener">Mã nguồn và cách mở bản local ↗</a>')
    html = html.replace('Demo suy luận từ CSV qua mô hình đã lưu ở seed 42.', 'Bản online suy luận ngay trong trình duyệt từ tham số mô hình seed 42 đã xuất. CSV bạn mở được xử lý tại máy, không tải lên máy chủ. Bản local dùng API Python.')
    html = html.replace('Demo suy luận từ CSV qua model đã lưu;', 'Demo suy luận từ CSV qua tham số model đã lưu;')
    for suffix in ('#page=23', '#page=24', ''):
        html = html.replace(f'href="assets/BAO_CAO_DOT3.pdf{suffix}"', f'href="{policy["round3_url"]}"')
    html = html.replace('Đối chiếu phương pháp · PDF trang 23 ↗', 'Đối chiếu phương pháp · trang 23 trong PDF trên Drive ↗')
    html = html.replace('Đối chiếu phương pháp và chỉ số ↗', 'Đối chiếu phương pháp và chỉ số · Drive ↗')
    html = html.replace('Báo cáo đợt 3 · bản đã gửi · 62 trang ↗', 'Báo cáo đợt 3 · bản đã gửi trên Drive · cần quyền xem ↗')
    (destination / 'index.html').write_text(html, encoding='utf-8')

    # Public hub excludes the local/offline study and review UI.
    hub = (source / 'ho-so-public.html').read_text(encoding='utf-8')
    for token, key in (('PRIVATE_REPORTS_URL', 'reports_url'), ('PRIVATE_ROOT_URL', 'root_url')):
        hub = hub.replace('{{' + token + '}}', policy[key])
    (destination / 'ho-so.html').write_text(hub, encoding='utf-8')

    provenance = json.loads((source / 'SOURCE_DATA.json').read_text(encoding='utf-8'))
    provenance['source_files'] = [row for row in provenance['source_files'] if Path(row['path']).suffix not in ('.pdf', '.zip', '.md')]
    provenance['private_documents_url'] = policy['reports_url']
    provenance['inference']['public_engine'] = 'browser-parameters-v1: Web Worker, no CSV upload'
    provenance['inference']['export_manifest'] = 'models/manifest.json'
    provenance['inference']['local_engine'] = 'Python API: /api/lab/run and /api/predict'
    (destination / 'SOURCE_DATA.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    write_static_host_files(destination, source)
    return destination


if __name__ == '__main__':
    print('Public demo assets prepared', build())
