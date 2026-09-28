"""Validate generated pages, navigation targets, media and canonical routes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import argparse,json

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.ids=[]; self.links=[]; self.h1=0; self.lang=''; self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='html':self.lang=a.get('lang')
        for key in ['src','href']:
            if a.get(key):self.links.append(a[key])

def check(output):
    output=Path(output).resolve(); files=json.loads((output/'._generated-pages.json').read_text())
    pages={name:Page((output/name).read_text(encoding='utf-8')) for name in files}
    errors=[]; checked=0
    for name,page in pages.items():
        if page.h1!=1:errors.append(f'{name}: expected one h1, got {page.h1}')
        if page.lang!='en':errors.append(f'{name}: language must be English')
        if len(page.ids)!=len(set(page.ids)):errors.append(f'{name}: duplicate IDs')
        for link in page.links:
            parts=urlsplit(link)
            if parts.scheme or parts.netloc:continue
            target=((output/name).parent/unquote(parts.path)).resolve() if parts.path else output/name
            if not target.is_relative_to(output):errors.append(f'{name}: link escapes output: {link}');continue
            if target.is_dir():target=target/'index.html'
            if not target.exists():errors.append(f'{name}: missing target: {link}');continue
            if parts.fragment and target.suffix=='.html':
                target_page=pages.get(str(target.relative_to(output)).replace('\\','/'))
                if target_page and unquote(parts.fragment) not in target_page.ids:errors.append(f'{name}: missing anchor: {link}')
            checked+=1
    if errors:raise AssertionError('\n'.join(errors))
    print(f'Validated {len(pages)} English pages and {checked} local links/media references.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='_site');args=ap.parse_args();check(args.output)
