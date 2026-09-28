"""Build the portfolio from Markdown into ordinary GitHub Pages-compatible HTML."""
from pathlib import Path
from string import Template
from urllib.parse import quote, unquote, urlsplit
from datetime import date
import argparse, html, json, re, shutil, unicodedata
import yaml
from markdown_it import MarkdownIt

ROOT=Path(__file__).resolve().parents[1]
MISSING=[]
escape=lambda value:html.escape(str(value),quote=True)

def read_document(path):
    text=path.read_text(encoding='utf-8')
    match=re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$',text,re.S)
    if not match: raise ValueError(f'{path}: YAML front matter is required')
    meta=yaml.safe_load(match[1])
    if not isinstance(meta,dict): raise ValueError(f'{path}: invalid front matter')
    return meta,match[2]

def slugify(text):
    text=unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',text).strip('-') or 'section'

def asset_exists(path,source):
    if urlsplit(path).scheme: return True
    target=(ROOT/unquote(path)).resolve()
    if not target.is_relative_to(ROOT): raise ValueError(f'Asset outside project: {path}')
    if target.is_file(): return True
    MISSING.append({'source':source,'path':path}); return False

def local_url(path,root):
    if urlsplit(path).scheme or path.startswith('#'): return path
    return root+quote(unquote(path),safe='/#?=&')

def block_math(state,start,end,silent):
    line=state.src[state.bMarks[start]+state.tShift[start]:state.eMarks[start]].strip()
    if not line.startswith('$$'): return False
    if silent: return True
    text=line[2:]; next_line=start+1
    if text.rstrip().endswith('$$'):
        content=text.rstrip()[:-2]
    else:
        parts=[text]
        while next_line<end:
            current=state.src[state.bMarks[next_line]:state.eMarks[next_line]].strip()
            next_line+=1
            if current.endswith('$$'):
                parts.append(current[:-2]); break
            parts.append(current)
        else: raise ValueError('A display equation is missing its closing $$ delimiter')
        content='\n'.join(parts)
    token=state.push('math_block','div',0); token.content=content.strip(); token.block=True
    state.line=next_line; return True

def inline_math(state,silent):
    if not state.src.startswith('\\(',state.pos): return False
    end=state.src.find('\\)',state.pos+2)
    if end<0: return False
    if not silent:
        token=state.push('math_inline','span',0); token.content=state.src[state.pos+2:end]
    state.pos=end+2; return True

def markdown(body,root='',source=''):
    parser=MarkdownIt('commonmark',{'html':True}).enable(['table','strikethrough'])
    parser.block.ruler.before('fence','math_block',block_math,{'alt':['paragraph','reference','blockquote','list']})
    parser.inline.ruler.before('escape','math_inline',inline_math)
    parser.add_render_rule('math_block',lambda self,t,i,o,e:f'<div class="math math-display" data-display="true">{escape(t[i].content)}</div>\n')
    parser.add_render_rule('math_inline',lambda self,t,i,o,e:f'<span class="math">{escape(t[i].content)}</span>')
    parser.add_render_rule('table_open',lambda *args:'<div class="table-scroll" role="region" aria-label="Data table" tabindex="0"><table>\n')
    parser.add_render_rule('table_close',lambda *args:'</table></div>\n')
    tokens=parser.parse(body)
    used={}
    for i,token in enumerate(tokens):
        if token.type=='heading_open':
            title=tokens[i+1].content; ident=slugify(title); used[ident]=used.get(ident,0)+1
            if used[ident]>1: ident+=f'-{used[ident]}'
            token.attrSet('id',ident)
        if token.type!='inline': continue
        children=token.children or []
        # A standalone image becomes an accessible, captioned figure.
        if len(children)==1 and children[0].type=='image' and i>0 and tokens[i-1].type=='paragraph_open':
            image=children[0]; path=image.attrGet('src'); alt=image.content
            caption=image.attrGet('title') or alt
            if asset_exists(path,source):
                url=escape(local_url(path,root))
                output=f'<figure class="project-figure"><a class="image-zoom" href="{url}" aria-label="Enlarge: {escape(alt)}"><img src="{url}" alt="{escape(alt)}" loading="lazy" decoding="async"></a><figcaption>{escape(caption)}</figcaption></figure>\n'
            else: output=''
            tokens[i-1].type='html_block'; tokens[i-1].content=output; tokens[i-1].nesting=0
            token.type='html_block'; token.content=''; tokens[i+1].hidden=True
            continue
        # Markdown video links also work as inline playback, without raw HTML.
        if len(children)==3 and children[0].type=='link_open' and children[-1].type=='link_close' and urlsplit(children[0].attrGet('href')).path.lower().endswith(('.mp4','.webm')) and tokens[i-1].type=='paragraph_open':
            path=children[0].attrGet('href'); caption=children[1].content
            output=''
            if asset_exists(path,source):
                url=escape(local_url(path,root))
                output=f'<figure class="project-figure"><video controls preload="metadata" playsinline aria-label="{escape(caption)}"><source src="{url}"><a href="{url}">{escape(caption)}</a></video><figcaption>{escape(caption)}</figcaption></figure>'
            tokens[i-1].type='html_block'; tokens[i-1].content=output; tokens[i-1].nesting=0
            token.type='html_block'; token.content=''; tokens[i+1].hidden=True
            continue
        for child in children:
            if child.type=='link_open': child.attrSet('href',local_url(child.attrGet('href'),root))
            if child.type=='image': child.attrSet('src',local_url(child.attrGet('src'),root))
    rendered=parser.renderer.render(tokens,parser.options,{})
    # Media-only sections are restored automatically when the assets are supplied.
    rendered=re.sub(r'<h([23])\b[^>]*>[^<]*</h\1>\s*(?=<h[23]\b|$)','',rendered)
    toc=[(ident,re.sub('<[^>]*>','',title)) for ident,title in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',rendered,re.S)]
    return rendered,toc,'class="math' in rendered

def load_projects(content_root=ROOT/'content/projects'):
    projects=[]; slugs=set(); aliases=set()
    for path in sorted(content_root.glob('*.md')):
        p,body=read_document(path)
        for key in ['title','slug','summary','discipline','role']:
            if not isinstance(p.get(key),str) or not p[key].strip(): raise ValueError(f'{path.name}: {key} must be text')
        if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',p['slug']): raise ValueError(f'{path.name}: invalid slug')
        if p['slug'] in slugs: raise ValueError(f'Duplicate slug: {p["slug"]}')
        slugs.add(p['slug'])
        for key in ['draft','featured']:
            if not isinstance(p.get(key,False),bool): raise ValueError(f'{path.name}: {key} must be true or false')
        if p.get('draft',False): continue
        if p.get('status','completed') not in ['completed','ongoing']: raise ValueError(f'{path.name}: invalid status')
        legacy=p.get('legacy','')
        if legacy:
            if not re.fullmatch(r'page\d+\.html',legacy) or legacy in aliases: raise ValueError(f'{path.name}: invalid or duplicate legacy alias')
            aliases.add(legacy)
        for key in ['tools','methods','tags']:
            if not isinstance(p.get(key,[]),list): raise ValueError(f'{path.name}: {key} must be a list')
            if any(not isinstance(label,str) or not label.strip() for label in p.get(key,[])): raise ValueError(f'{path.name}: {key} must contain non-empty text labels')
        p.update(body=body,source=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),url=f'case-studies/{p["slug"]}/index.html')
        p.setdefault('short_title',p['title']); p.setdefault('cover',''); p.setdefault('cover_alt',p['title'])
        p.setdefault('order',100); p.setdefault('tools',[]); p.setdefault('methods',[]); p.setdefault('tags',[])
        p.setdefault('status','completed'); p.setdefault('period',''); p.setdefault('featured',False)
        if type(p['order']) is not int: raise ValueError(f'{path.name}: order must be a number')
        projects.append(p)
    return sorted(projects,key=lambda p:(p['order'],p['title']))

def cover(p,root='',eager=False):
    if p['cover'] and asset_exists(p['cover'],p['source']):
        return f'<div class="cover-image"><img src="{escape(local_url(p["cover"],root))}" alt="{escape(p["cover_alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}></div>'
    short={'gyroid-structures':'GYROID','mql-project':'MQL','quadruped-robot':'QUADRUPED','arduino-drone':'ARDUINO'}.get(p['slug'],p['short_title'])
    return f'<div class="cover-type cover-{escape(p["discipline"].lower())}" aria-hidden="true"><span class="cover-axis">{escape(p["discipline"])} / Study</span><strong>{escape(short)}</strong><span class="cover-method">{escape(" / ".join(p["methods"][:2]))}</span><i></i></div>'

def project_labels(p):
    return list(dict.fromkeys([p['discipline'],*p.get('tags',[])]))

def row(p,index,root='',filterable=False):
    data=''
    if filterable:
        search=' '.join([p['title'],p['summary'],*project_labels(p),*p['tools'],*p['methods']])
        data=f' data-project data-disciplines="{escape(json.dumps(project_labels(p)))}" data-search="{escape(search.lower())}"'
    return f'''<article class="work-row"{data}><a href="{root}{p['url']}" class="work-link">
      <div class="work-thumb">{cover(p,root)}</div><span class="work-number">{index:02}</span>
      <div class="work-description"><p class="eyebrow">{escape(' / '.join(project_labels(p)))}</p><h3>{escape(p['short_title'])}</h3><p>{escape(p['summary'])}</p></div>
      <span class="work-methods">{escape(' / '.join(p['methods']))}</span><span class="work-arrow" aria-hidden="true">↗</span></a></article>'''

def home(projects,config):
    selected=[p for p in projects if p['featured']][:3] or projects[:3]
    selected_slugs={p['slug'] for p in selected}
    remaining=[p for p in projects if p['slug'] not in selected_slugs]
    landing=config['landing']
    panels=[]; tabs=[]
    for i,p in enumerate(selected):
        number=projects.index(p)+1
        panels.append(f'''<div class="hero-project" role="tabpanel" id="project-panel-{i}" aria-labelledby="project-tab-{i}" {"hidden" if i else ""}>
          <a class="hero-art" href="{p['url']}">{cover(p,eager=i==0)}<span class="hero-counter">Study {number:02}</span><span class="hero-open">Explore the study <span aria-hidden="true">↗</span></span></a>
          <div class="hero-project-caption"><span>{escape(' / '.join(project_labels(p)))}</span><span>{escape(' / '.join(p['methods']))}</span></div>
          <div class="hero-project-detail"><h2><a href="{p['url']}">{escape(p['short_title'])}</a></h2><p>{escape(p['summary'])}</p></div></div>''')
        tabs.append(f'<button type="button" role="tab" id="project-tab-{i}" aria-controls="project-panel-{i}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}"><span>{number:02}</span>{escape(p["short_title"])}</button>')
    cards=[]
    for p in remaining[:3]:
        number=projects.index(p)+1
        cards.append(f'''<article class="explore-card" data-home-study="{escape(p['slug'])}"><a href="{p['url']}"><div class="explore-art">{cover(p)}<span class="explore-number">{number:02}</span><span class="explore-open" aria-hidden="true">↗</span></div><div class="explore-copy"><p class="eyebrow">{escape(' / '.join(project_labels(p)))}</p><h3>{escape(p['short_title'])}</h3><p>{escape(p['summary'])}</p><span class="explore-methods">{escape(' / '.join(p['methods']))}</span></div></a></article>''')
    more=f'''<section class="shell explore-section" id="projects"><div class="landing-section-head"><div><p class="eyebrow">Further explorations</p><h2>More to explore<span class="accent">.</span></h2></div><p>More projects, experiments<br>and lessons from the work.</p></div><div class="explore-grid">{''.join(cards)}</div><div class="explore-end"><span>{len(projects):02} studies across design, analysis and mechatronics</span><a class="text-link" href="work.html">Browse the complete index <span aria-hidden="true">↗</span></a></div></section>''' if cards else ''
    capabilities=[]
    for i,c in enumerate(landing['capabilities']):
        query='discipline='+quote(c['filter']) if c.get('filter') else 'q='+quote(c['search'])
        capabilities.append(f'''<a class="capability" href="work.html?{query}"><span class="capability-number">0{i+1}</span><h3>{escape(c['title'])}</h3><p>{escape(c['description'])}</p><span class="capability-tools">{escape(c['tools'])}</span><span class="capability-arrow" aria-hidden="true">↗</span></a>''')
    capabilities=''.join(capabilities)
    return f'''<section class="hero" id="featured"><div class="shell hero-layout"><div class="hero-intro"><p class="eyebrow">Mechatronics engineer / Selected work</p><h1>Design.<br> Analyse.<br> Make<span class="accent">.</span></h1><p class="hero-description">{escape(config['intro'])}</p><div class="hero-actions"><a class="landing-button" href="work.html">Explore the work <span aria-hidden="true">↗</span></a><a class="hero-about-link" href="#approach">My approach <span aria-hidden="true">↓</span></a></div><span class="hero-footnote">Based in {escape(config['location'])}</span></div><div class="hero-showcase">{''.join(panels)}<div class="project-tabs" role="tablist" aria-label="Featured projects">{''.join(tabs)}</div></div></div><div class="shell hero-bottom"><span>Selected engineering work / {len(projects):02} studies</span><a href="#approach">Discover the thinking behind the work <span aria-hidden="true">↓</span></a></div></section>
    <section class="shell approach-section" id="approach"><div class="landing-section-head"><div><p class="eyebrow">The approach</p><h2>{escape(landing['approach_title'])}</h2></div><p>{escape(landing['approach_intro'])}</p></div><div class="capabilities">{capabilities}</div></section>
    {more}
    <section class="home-profile" id="about"><div class="shell home-profile-grid"><div class="home-portrait"><img src="images/linkedin_pp.jpeg" alt="Burak Taş" width="450" height="450" loading="lazy" decoding="async"><span>Istanbul, Türkiye</span></div><div class="home-profile-copy"><p class="eyebrow">Behind the work / Burak Taş</p><h2>{escape(landing['profile_intro'])}</h2><p>{escape(landing['profile_text'])}</p><div class="inline-links"><a class="text-link" href="about.html">More about me ↗</a><a class="text-link" href="{config['cv']}">View my CV ↗</a></div></div></div></section>
<section class="home-contact" id="contact"><div class="shell"><div class="home-contact-intro"><p class="eyebrow">Continue the conversation</p><p>A project, an opportunity or a question about my work?</p></div><a class="home-contact-title" href="contact.html">Let's connect<span class="accent">.</span><span class="contact-arrow" aria-hidden="true">↗</span></a><div class="home-contact-links"><a href="{escape(config['linkedin'])}">Find me on LinkedIn ↗</a></div></div></section>'''

def work(projects):
    categories=sorted({label for p in projects for label in project_labels(p)})
    filters='<button type="button" data-filter="all" aria-pressed="true">All studies</button>'+''.join(f'<button type="button" data-filter="{escape(c)}" aria-pressed="false">{escape(c)}</button>' for c in categories)
    rows=''.join(row(p,i+1,filterable=True) for i,p in enumerate(projects))
    return f'''<section class="shell work-index"><div class="page-intro"><div><p class="eyebrow">Selected engineering work</p><h1>Work index<span class="accent">.</span></h1></div><p>Design decisions, supporting analysis<br>and lessons from the work.</p></div>
      <div class="work-controls" data-js-only hidden><div class="filters" role="group" aria-label="Filter by discipline">{filters}</div><label class="search-label"><span class="sr-only">Search projects or methods</span><input type="search" id="project-search" placeholder="Search projects or methods…" autocomplete="off"><span aria-hidden="true">↗</span></label></div>
      <p class="result-count" id="result-count" role="status" aria-live="polite">{len(projects):02} selected studies</p><div class="work-list">{rows}</div>
      <div class="empty-state" hidden><h2>No matching studies.</h2><p>Try another project, tool or discipline.</p><button type="button" class="text-link" id="clear-filters">Clear search and filters ↗</button></div></section>'''

def case_study(p,projects,root):
    rendered,toc,math=markdown(p['body'],root,p['source'])
    toc_links=''.join(f'<li><a href="#{ident}">{escape(title)}</a></li>' for ident,title in toc)
    number=projects.index(p)+1
    position=projects.index(p); following=projects[(position+1)%len(projects)] if len(projects)>1 else None
    next_link=f'<a href="{root}{following["url"]}"><span class="eyebrow">Next study</span><strong>{escape(following["short_title"])} <span aria-hidden="true">↗</span></strong></a>' if following else ''
    tools=''.join(f'<li>{escape(t)}</li>' for t in dict.fromkeys([*p['tools'],*p.get('tags',[])]))
    words=len(re.findall(r'\w+',p['body'])); minutes=max(1,round(words/200))
    return f'''<article class="case-study"><header class="shell case-header"><div class="case-breadcrumb"><a href="{root}work.html">← Work index</a><span>{escape(p['discipline'])} / Case study {number:02}</span></div><div class="case-hero"><div><p class="eyebrow">{escape(' / '.join(p['methods']))}</p><h1>{escape(p['short_title'])}</h1><p class="case-summary">{escape(p.get('subtitle',p['summary']))}</p><dl class="case-facts"><div><dt>My contribution</dt><dd>{escape(p['role'])}</dd></div><div><dt>Status / Period</dt><dd>{'In progress' if p['status']=='ongoing' else 'Completed'}{(' · '+escape(p['period'])) if p['period'] and p['period']!='In progress' else ''}</dd></div></dl><p class="read-time">{minutes} min read · {escape(p['discipline'])}</p></div><div class="case-cover">{cover(p,root,True)}</div></div></header>
      <div class="shell article-layout"><aside class="article-aside"><nav class="desktop-toc" aria-label="In this study"><p class="eyebrow">In this study</p><ol>{toc_links}</ol></nav><details class="mobile-toc"><summary>In this study <span aria-hidden="true">+</span></summary><nav aria-label="Study sections"><ol>{toc_links}</ol></nav></details></aside>
      <div class="article-main"><div class="prose">{rendered}</div><section class="tools-section"><h2>Tools & methods</h2><ul>{tools}</ul></section><nav class="study-pagination" aria-label="More studies">{next_link}<a class="text-link" href="{root}work.html">Back to work index ↗</a></nav></div></div></article>''',math

def about(config):
    meta,body=read_document(ROOT/'content/pages/about.md'); rendered,_,math=markdown(body,source='content/pages/about.md')
    return f'''<section class="shell about-page"><div class="page-intro"><div><p class="eyebrow">About</p><h1>{escape(meta['title'])}<span class="accent">.</span></h1></div><p>{escape(config['location'])}<br>Design / Analysis / Prototyping</p></div><div class="about-layout"><aside><img class="portrait" src="images/linkedin_pp.jpeg" alt="Burak Taş" width="450" height="450"><h2>Burak Taş</h2><p>Mechatronics Engineer</p><div class="inline-links"><a class="text-link" href="{config['cv']}">View CV ↗</a><a class="text-link" href="contact.html">Contact ↗</a></div></aside><div class="prose">{rendered}</div></div></section>''',math

def contact(config):
    meta,body=read_document(ROOT/'content/pages/contact.md'); rendered,_,math=markdown(body,source='content/pages/contact.md')
    return f'''<section class="shell contact-page"><p class="eyebrow">Contact / Get in touch</p><h1>{escape(meta['title'])}</h1><div class="contact-layout"><div class="prose">{rendered}</div><div class="contact-details"><a class="contact-email" href="mailto:{config['email']}">{escape(config['email'])}<span aria-hidden="true">↗</span></a><dl><div><dt>Location</dt><dd>{escape(config['location'])}</dd></div></dl><div class="inline-links"><a class="text-link" href="{config['linkedin']}">LinkedIn ↗</a><a class="text-link" href="{config['github']}">GitHub ↗</a><a class="text-link" href="{config['cv']}">CV (PDF) ↗</a></div></div></div></section>''',math

def build(output,preview_drafts=False):
    MISSING.clear(); config=yaml.safe_load((ROOT/'content/site.yml').read_text(encoding='utf-8'))
    projects=load_projects()
    if not projects: raise ValueError('At least one published project is required')
    output=Path(output).resolve(); output.mkdir(parents=True,exist_ok=True)
    base=Template((ROOT/'templates/base.html').read_text(encoding='utf-8'))
    generated=[]
    def page(path,title,description,content,kind='',math=False,canonical=None):
        root='../'*(len(Path(path).parts)-1)
        canonical=config['url'].rstrip('/')+'/'+(canonical or path)
        assets=f'<link rel="stylesheet" href="{root}assets/vendor/katex/katex.min.css"><script defer src="{root}assets/vendor/katex/katex.min.js"></script><script defer src="{root}assets/math.js"></script>' if math else ''
        result=base.substitute(title=escape(title+' — '+config['name']),description=escape(description),canonical=escape(canonical),og_type='article' if kind=='case' else 'website',og_image=escape(config['url']+'/images/magazine.png'),root=root,math_assets=assets,landing_assets='<link rel="stylesheet" href="assets/landing.css">' if kind=='home' else '',body_class=kind,content=content,work_current='aria-current="page"' if kind=='work' else '',about_current='aria-current="page"' if kind=='about' else '',contact_current='aria-current="page"' if kind=='contact' else '',cv=escape(root+config['cv']),name=escape(config['name']),profession=escape(config['profession']),linkedin=escape(config['linkedin']),github=escape(config['github']),email=escape(config['email']),year=date.today().year)
        result=result.replace('<meta charset="utf-8">','<meta charset="utf-8">\n  <meta name="generator" content="Portfolio Markdown">')
        target=output/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(result,encoding='utf-8'); generated.append(path)
    page('index.html','Selected engineering work',config['intro'],home(projects,config),'home')
    page('work.html','Work index','Selected engineering case studies in mechanical design, analysis, manufacturing and robotics.',work(projects),'work')
    for name,fn in [('about',about),('contact',contact)]:
        content,math=fn(config); page(name+'.html',name.title(),config['bio'] if name=='about' else 'Get in touch with Burak Taş, Mechatronics Engineer.',content,name,math)
    for p in projects:
        content,math=case_study(p,projects,'../../'); page(p['url'],p['title'],p['summary'],content,'case',math)
        if p.get('legacy'):
            content,math=case_study(p,projects,''); page(p['legacy'],p['title'],p['summary'],content,'case',math,p['url'])
    # Absolute project paths make the GitHub Pages 404 work at any requested depth.
    error=f'<section class="shell error-page"><p class="eyebrow">404 / Page not found</p><h1>A different direction<span class="accent">.</span></h1><p>This page could not be found. Explore the selected engineering work instead.</p><a class="text-link" href="{config["url"]}/work.html">Open the work index ↗</a></section>'
    page('404.html','Page not found','This page could not be found.',error,'error')
    errfile=output/'404.html'; errfile.write_text(re.sub(r'(href|src)="(?!(?:https?:|mailto:|tel:|#))',lambda m:m[1]+'="'+config['url'].rstrip('/')+'/',errfile.read_text(encoding='utf-8')),encoding='utf-8')
    manifest=output/'._generated-pages.json'
    if manifest.exists():
        for old in json.loads(manifest.read_text(encoding='utf-8')):
            target=(output/old).resolve()
            if old not in generated and target.is_relative_to(output) and target.is_file() and '<meta name="generator" content="Portfolio Markdown">' in target.read_text(encoding='utf-8'):
                target.unlink()  # Only obsolete pages created by this builder.
    manifest.write_text(json.dumps(generated,indent=2),encoding='utf-8')
    if output!=ROOT:
        for folder in ['assets','images','pdf']: shutil.copytree(ROOT/folder,output/folder,dirs_exist_ok=True)
    (output/'.nojekyll').write_text('',encoding='utf-8')
    urls=[p for p in generated if not re.fullmatch(r'page\d+\.html',p) and p!='404.html']
    (output/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{escape(config["url"]+"/"+p)}</loc></url>' for p in urls)+'</urlset>',encoding='utf-8')
    report=list({(m['source'],m['path']):m for m in MISSING}.values())
    (ROOT/'docs/missing-media.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Built {len(generated)} pages from {len(projects)} published Markdown projects into {output}')
    if report: print(f'{len(report)} missing media references retained in Markdown; see docs/missing-media.json.')
    return generated

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--output',default=str(ROOT/'_site'),help='Output directory (use . to update the root HTML files)')
    args=ap.parse_args(); build(args.output)
