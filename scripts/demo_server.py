"""Loopback-only teaching demo; no training, remote APIs, or writes to runs."""
import argparse
import json
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from nids_benchmark.demo import predict_csv,compare_csv
from nids_benchmark.application import catalog,run_case


class Handler(BaseHTTPRequestHandler):
    def reply(self,status,data,kind='application/json; charset=utf-8'):
        payload=data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False,allow_nan=False).encode('utf-8')
        self.send_response(status);self.send_header('Content-Type',kind)
        self.send_header('Content-Length',str(len(payload)))
        self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(payload)

    def do_GET(self):
        path=urlparse(self.path).path
        if path in ('/','/index.html'):
            self.reply(200,(ROOT/'demo/index.html').read_bytes(),'text/html; charset=utf-8')
        elif path in ('/lab','/lab/'):
            self.reply(200,(ROOT/'demo/lab.html').read_bytes(),'text/html; charset=utf-8')
        elif path=='/presentation':
            self.send_response(302);self.send_header('Location','/presentation/');self.end_headers()
        elif path.startswith('/presentation/'):
            # Serve only this self-contained presentation, never the repository root.
            relative=unquote(path[len('/presentation'):]).lstrip('/') or 'index.html'
            allowed={'index.html','data.js','presentation.js','presentation.css','SOURCE_DATA.json',
                     'assets/AP_MEAN_STD.csv','assets/OPERATING_POINTS_MEAN_STD.csv','assets/BAO_CAO_DOT3.pdf',
                     'ho-so.html','ho-so.css','ho-so.js'}
            release=ROOT/'docs/releases/review_final_20261113'
            downloads={f'downloads/{item.name}':item for folder in ('reports','slides')
                       for item in (release/folder).iterdir()
                       if item.is_file() and item.suffix in ('.pdf','.zip')}
            downloads.update({f'downloads/{name}':ROOT/'docs/management'/name
                              for name in ('BAN_GIAO_BAO_VE_20261113.md','DOI_CHIEU_YEU_CAU_20261114.md')})
            if relative in allowed:
                target=ROOT/'demo/presentation'/relative
                if target.is_file():
                    self.reply(200,target.read_bytes(),mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
                else:self.reply(404,{'error':'Tệp trình bày chưa có trên máy.'})
            elif relative in downloads:
                target=downloads[relative]
                if target.is_file():
                    self.reply(200,target.read_bytes(),mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
                else:self.reply(404,{'error':'Tệp hồ sơ chưa có trên máy.'})
            else:self.reply(404,{'error':'Không có tệp trình bày này.'})
        elif path=='/api/lab/catalog':self.reply(200,catalog())
        elif path=='/health': self.reply(200,{'status':'ok','app':'nids-demo','seed':42})
        elif path=='/sample.csv': self.reply(200,(ROOT/'demo/sample.csv').read_bytes(),'text/csv; charset=utf-8')
        elif path=='/favicon.ico': self.reply(204,b'')
        elif path.startswith('/bo/'):
            package=(ROOT.parent/'02_Bao_cao/BO_HO_SO_NHOM_20261025').resolve()
            target=(package/unquote(path[4:])).resolve()
            if target.is_relative_to(package) and target.is_file() and target.suffix.lower() in ('.html','.pdf','.png','.jpg','.json','.csv','.ps1','.txt'):
                self.reply(200,target.read_bytes(),mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
            else:self.reply(404,{'error':'Không có tệp trong bộ báo cáo.'})
        else: self.reply(404,{'error':'Không có trang này.'})

    def do_POST(self):
        route=urlparse(self.path).path
        if route not in ('/api/predict','/api/compare','/api/lab/run'): return self.reply(404,{'error':'Không có chức năng này.'})
        try:
            if self.headers.get('Origin') not in (None,f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'):
                return self.reply(403,{'error':'Chỉ dùng từ trang demo trên máy này.'})
            length=int(self.headers.get('Content-Length','0'))
            if length<1 or length>2_000_000: raise ValueError('CSV quá lớn hoặc chưa có nội dung.')
            try:
                payload=json.loads(self.rfile.read(length).decode('utf-8'))
            except json.JSONDecodeError as exc:
                raise ValueError('Nội dung yêu cầu không phải JSON hợp lệ.') from exc
            if not isinstance(payload,dict):
                raise ValueError('Nội dung yêu cầu phải là một đối tượng JSON.')
            if route in ('/api/predict','/api/compare') and not isinstance(payload.get('csv',''),str):
                raise ValueError('Nội dung CSV phải là văn bản.')
            if route=='/api/lab/run':
                result=run_case(payload.get('case','mixed'),payload.get('scenario','CS'),payload.get('model','RF'),float(payload.get('target',.05)))
            elif route=='/api/compare':
                result=compare_csv(payload.get('scenario','CS'),float(payload.get('target',.05)),payload.get('csv',''))
            else:
                result=predict_csv(payload.get('scenario','CS'),payload.get('model','RF'),float(payload.get('target',.05)),payload.get('csv',''))
            self.reply(200,result)
        except (ValueError,KeyError,TypeError,UnicodeDecodeError) as exc: self.reply(400,{'error':str(exc)})
        except Exception: self.reply(500,{'error':'Không tải/chạy được mô hình. Kiểm thư viện và model bundle trên máy.'})


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4397);args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'NIDS demo: http://127.0.0.1:{args.port}',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
