"""Restore missing images from the owner's public repository; keep local files."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib
import json
import requests

ROOT = Path(__file__).resolve().parents[1]


def restore(item):
    relative = PurePosixPath(item['path'])
    target = (ROOT / relative).resolve()
    if not target.is_relative_to(ROOT / 'images'):
        raise ValueError('Unexpected media path')
    if target.exists():
        return None
    response = requests.get(
        'https://raw.githubusercontent.com/burkutken/portfolio/main/'
        + quote(item['path'], safe='/'), timeout=120)
    response.raise_for_status()
    data = response.content
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if digest != item['sha']:
        raise ValueError(f"Git blob checksum mismatch: {item['path']}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {'path': item['path'], 'bytes': len(data), 'git_blob': digest}


if __name__ == '__main__':
    tree = json.loads((ROOT / 'artifacts/github-tree.json').read_text(encoding='utf-8'))
    items = [item for item in tree['tree']
             if item['type'] == 'blob' and item['path'].startswith('images/')]
    with ThreadPoolExecutor(max_workers=4) as pool:
        restored = [result for result in pool.map(restore, items) if result]
    (ROOT / 'artifacts/restored-media.json').write_text(
        json.dumps(restored, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Restored {len(restored)} missing files ({sum(x["bytes"] for x in restored):,} bytes).')
