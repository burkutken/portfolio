"""Fetch a pinned, self-hosted KaTeX distribution (run only when updating vendors)."""
from pathlib import Path
from urllib.request import urlopen
import io, tarfile

ROOT=Path(__file__).resolve().parents[1]
VERSION='0.16.22'
URL=f'https://registry.npmjs.org/katex/-/katex-{VERSION}.tgz'
def main():
    data=urlopen(URL,timeout=30).read()
    target=ROOT/'assets/vendor/katex'; target.mkdir(parents=True,exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as archive:
        for item in archive.getmembers():
            name=item.name
            if name in ['package/dist/katex.min.js','package/dist/katex.min.css','package/LICENSE'] or name.startswith('package/dist/fonts/'):
                relative=name.removeprefix('package/dist/').removeprefix('package/')
                dest=(target/relative).resolve()
                if not dest.is_relative_to(target.resolve()) or not item.isfile(): raise ValueError('Unexpected archive entry')
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(archive.extractfile(item).read())
    (target/'VERSION').write_text(VERSION+'\n',encoding='utf-8')
    print('Vendored KaTeX',VERSION)
if __name__=='__main__': main()
