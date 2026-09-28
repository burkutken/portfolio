"""Build and serve a local preview; rebuild when authoring files change."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import argparse,threading,time
from build import ROOT,build

def fingerprint():
    files=[p for folder in ['content','templates','assets'] for p in (ROOT/folder).rglob('*') if p.is_file()]
    files.append(ROOT/'scripts/build.py')
    return tuple(sorted((str(p),p.stat().st_mtime_ns) for p in files))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8000);args=ap.parse_args()
    output=ROOT/'_site';build(output)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(SimpleHTTPRequestHandler,directory=str(output)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    print(f'Preview: http://127.0.0.1:{args.port}/ (Ctrl+C to stop)',flush=True)
    previous=fingerprint()
    try:
        while True:
            time.sleep(.8);current=fingerprint()
            if current!=previous:
                try:build(output);print('Rebuilt. Refresh the browser.',flush=True)
                except Exception as error:print(f'Build failed: {error}',flush=True)
                previous=current
    except KeyboardInterrupt:pass
    finally:server.shutdown()
if __name__=='__main__':main()
