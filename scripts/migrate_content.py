"""One-time, lossless prose migration from the archived portfolio HTML."""
from pathlib import Path
from html.parser import HTMLParser
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]

class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []
    def text(self):
        return re.sub(r'\s+', ' ', ''.join(c.text() if isinstance(c, Node) else c for c in self.children)).strip()
    def find(self, tag=None, cls=None):
        return next(iter(self.all(tag, cls)), None)
    def all(self, tag=None, cls=None):
        for c in self.children:
            if isinstance(c, Node):
                if (not tag or c.tag == tag) and (not cls or cls in c.attrs.get('class','').split()):
                    yield c
                yield from c.all(tag, cls)

class Tree(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node(); self.stack = [self.root]; self.feed(source)
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs); self.stack[-1].children.append(n)
        if tag not in ['img','source','br','hr','meta','link','input']: self.stack.append(n)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]; break
    def handle_data(self, data): self.stack[-1].children.append(data)

def md(n):
    if isinstance(n, str): return re.sub(r'\s+', ' ', n)
    if n.tag == 'a' and 'back-to-portfolio' in n.attrs.get('class',''): return ''
    if 'gallery-item' in n.attrs.get('class','').split():
        img=n.find('img'); cap=n.find(cls='gallery-caption')
        if not img: return ''
        title=cap.text() if cap else img.attrs.get('alt','Project image')
        src=re.sub('/+','/',img.attrs['src'])
        return f'\n\n![{img.attrs.get("alt",title)}](<{src}> "{title}")\n\n'
    if n.tag=='video':
        src=n.find('source')
        return f'\n\n[Watch project video](<{src.attrs["src"]}>)\n\n' if src else ''
    if n.tag=='img': return f'\n\n![{n.attrs.get("alt","")}](<{n.attrs["src"]}>)\n\n'
    body=''.join(md(c) for c in n.children).strip()
    if n.tag in ['h2','h3','h4']: return '\n\n'+'#'*int(n.tag[1])+' '+body+'\n\n'
    if n.tag=='p': return '\n\n'+body+'\n\n' if body else ''
    if n.tag=='li': return '\n- '+body+'\n'
    if n.tag in ['ul','ol']: return '\n\n'+body+'\n\n'
    if n.tag in ['strong','b']: return '**'+body+'**'
    if n.tag in ['em','i']: return '*'+body+'*' if body else ''
    if n.tag=='br': return '\n'
    return '\n'+body+'\n'

PROJECTS=[
    ('magazine-system','Magazine System','Mechanical','CAD / FEA / Control','Mechanical design, structural analysis and control development.','Design, analysis and control','images/magazine.png',1,True),
    ('quadruped-robot','Quadruped Robot','Robotics','CAD / Control / Prototyping','A quadruped robot concept combining mechanical design, sensors and control.','Mechanical design and control','images/quadruped robot/robodog_assem_2.png',4,False),
    ('mql-project','MQL Project','Manufacturing','CAD / CFD / Testing','Nozzle design, simulation and an experimental setup for minimum quantity lubrication.','Experimental setup and nozzle design','images/mql/fusion360_setup.png',3,True),
    ('gyroid-structures','Gyroid Structures','Manufacturing','Design / Experiment','Lattice geometry, SLA prototyping and compression testing.','Design, prototyping and testing','images/gyroid/gyroid_printed.png',2,True),
    ('arduino-drone','Arduino Drone','Robotics','Arduino / Programming / PoC','An Arduino-based brushed drone built as a hands-on introduction to robotics.','Embedded programming and prototyping','',5,False),
]

def migrate():
    records=[]
    for i,(slug,short,discipline,methods,summary,role,cover,order,featured) in enumerate(PROJECTS,1):
        tree=Tree((ROOT/f'archive/original-site/page{i}.html').read_text(encoding='utf-8')).root
        header=tree.find(cls='project-header'); detail=tree.find(cls='project-details')
        sidebar=tree.find(cls='project-sidebar'); gallery=tree.find(cls='project-gallery')
        stacks=list(sidebar.all(cls='tech-stack')) if sidebar else []
        tools=[n.text() for n in stacks[0].all(cls='tech-item')] if stacks else []
        meta=[n.text() for n in header.all(cls='meta-item')]
        period=next((t.replace('Completed: ','') for t in meta if t.startswith('Completed:')),'In progress')
        data=dict(title=header.find('h1').text(),short_title=short,slug=slug,summary=summary,
                  subtitle=header.find('p').text(),discipline=discipline,methods=methods.split(' / '),
                  tools=tools,role=role,period=period,status='ongoing' if i==4 else 'completed',
                  cover=cover,cover_alt=short,order=order,featured=featured,draft=False,legacy=f'page{i}.html')
        body=md(detail)
        if len(stacks)>1:
            body+='\n\n## Project timeline\n\n| Stage | Period |\n| --- | --- |\n'
            for item in stacks[1].all(cls='tech-item'):
                a,b=item.find('h4'),item.find('p')
                if a and b: body+=f'| {a.text()} | {b.text()} |\n'
        if gallery: body+='\n\n## Project gallery\n\n'+md(gallery)
        body=re.sub(r'\n[ \t]+','\n',body); body=re.sub(r'\n{3,}','\n\n',body).strip()
        # Verify every original prose paragraph and bullet survives the migration.
        compact=lambda t:re.sub(r'\s+',' ',t).strip()
        for node in detail.all():
            if node.tag in ['p','li'] and node.text():
                assert compact(node.text()) in compact(body), (slug,node.text())
        path=ROOT/f'content/projects/{slug}.md'
        path.write_text('---\n'+yaml.safe_dump(data,sort_keys=False,allow_unicode=True)+'---\n\n'+body+'\n',encoding='utf-8')
        records.append(f'- `{path.relative_to(ROOT)}` ← `page{i}.html`: all prose, lists, timeline and media references retained.')
    home=Tree((ROOT/'archive/original-site/index.html').read_text(encoding='utf-8')).root
    about=home.find(cls='about-text')
    paragraphs='\n\n'.join(n.text() for n in about.all('p'))
    skills=[n.text() for n in about.all(cls='skill')]
    (ROOT/'content/pages/about.md').write_text('---\ntitle: Behind the work\nsubtitle: Burak Taş — Mechatronics Engineer\n---\n\n'+paragraphs+'\n\n## Technical skills\n\n'+'\n'.join('- '+s for s in skills)+'\n',encoding='utf-8')
    (ROOT/'docs/MIGRATION.md').write_text('# Content migration\n\n'+ '\n'.join(records)+'''\n\nThe old HTML is archived in `archive/original-site/`. Existing technical statements have been migrated, not independently verified or expanded. No invented performance figures or new engineering analysis were added.

## Original content to review

- MQL: the Challenge paragraph describes a quadruped robot. It has been preserved to avoid silently changing the author’s content.
- MQL: the completion date and simulation/finalisation timeline are inconsistent.
- Gyroid: application and approval dates appear out of sequence. The project remains marked ongoing as in the original.
- Some gallery captions in MQL and Quadruped appear copied from other projects.
- Many media files referenced by the old HTML are not present in this local copy. References are retained in Markdown; absent media are omitted from the rendered page. `docs/missing-media.json` lists the missing paths. Adding a file at its original path and rebuilding restores it automatically.
- The original standalone contact page used example contact details. The replacement uses the real contact information from the original homepage.
''',encoding='utf-8')
    print('Migrated five complete case studies and the about page.')

if __name__=='__main__': migrate()
