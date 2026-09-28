"""Create a draft case study from the shared English Markdown template."""
from pathlib import Path
import argparse,re,yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('slug');ap.add_argument('--title',required=True);args=ap.parse_args()
    if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',args.slug):ap.error('Use lowercase words separated by hyphens for the slug.')
    path=ROOT/'content/projects'/f'{args.slug}.md'
    if path.exists():ap.error(f'{path.name} already exists; it has not been overwritten.')
    text=(ROOT/'templates/case-study.md').read_text(encoding='utf-8')
    _,front,body=text.split('---',2);meta=yaml.safe_load(front)
    meta.update(slug=args.slug,title=args.title,short_title=args.title,order=len(list((ROOT/'content/projects').glob('*.md')))+1)
    path.write_text('---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)+'---'+body,encoding='utf-8')
    print(f'Created {path.relative_to(ROOT)} (draft: true).')
if __name__=='__main__':main()
