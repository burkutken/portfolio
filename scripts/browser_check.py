"""Desktop/mobile checks using local Chrome, including a /portfolio/ base path."""
from pathlib import Path
import sys,threading,json
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.tools'))
from playwright.sync_api import sync_playwright
from build import markdown

def check_gyroid(page, url, dest):
    """Check the report-based study, including real media and technical content."""
    for width in [1440, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 1000})
        page.goto(url+'case-studies/gyroid-structures/index.html')
        page.locator('img[src]').evaluate_all('(images) => images.forEach(i => i.loading = "eager")')
        page.evaluate('async () => Promise.all([...document.querySelectorAll("img[src]")].map(i => i.decode()))')
        assert page.locator('.prose h2').count() == 7
        assert page.locator('.prose .table-scroll').count() == 4
        assert page.locator('.katex').count() == 6, 'Gyroid equations did not render'
        assert page.locator('math').count() == 6, 'Gyroid MathML missing'
        assert page.locator('.katex-error').count() == 0
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Gyroid overflow at {width}'
        assert 'Completed' in page.locator('.case-facts').inner_text()
        if width in [1440,390]:
            page.screenshot(path=str(dest/f'gyroid-{width}.png'),full_page=True,animations='disabled')
            page.screenshot(path=str(dest/f'gyroid-{width}-top.png'),animations='disabled')
        if width == 390:
            page.locator('.mobile-toc summary').click()
            page.locator('.mobile-toc a').filter(has_text='How far could prediction go?').click()
            assert page.url.endswith('#how-far-could-prediction-go')
            assert not page.locator('.mobile-toc').get_attribute('open')
    page.locator('.prose details summary').click()
    video = page.locator('.prose video')
    assert video.is_visible()
    page.wait_for_function('document.querySelector("video").readyState >= 1 || document.querySelector("video").error')
    assert video.evaluate('(v) => v.error === null && v.duration > 0'), 'Gyroid video cannot load'
    video.evaluate('(v) => { v.muted = true; return v.play(); }')
    page.wait_for_function('document.querySelector("video").currentTime > 0')
    video.evaluate('(v) => v.pause()')
    page.locator('.image-zoom').last.click()
    assert page.locator('dialog').is_visible()
    page.keyboard.press('Escape')
    assert not page.locator('dialog').is_visible()


def check_magazine(page, url, dest):
    """Verify the thesis-based contribution page and optional evidence figures."""
    contribution_sections = [
        'Magazine system design', 'Gripper static and shock analysis',
        'Magazine component static and shock analysis', 'Control system',
        'Linear actuator mechanism', 'Motor selection',
    ]
    for width in [1440, 768, 390, 320]:
        page.set_viewport_size({'width':width, 'height':1000})
        page.goto(url+'case-studies/magazine-system/index.html')
        page.locator('img[src]').evaluate_all('(images) => images.forEach(i => i.loading = "eager")')
        page.evaluate('async () => Promise.all([...document.querySelectorAll("img[src]")].map(i => i.decode()))')
        assert page.locator('.prose h2').count()==9
        headings=page.locator('.prose h2').all_text_contents()
        assert all(section in headings for section in contribution_sections)
        assert page.locator('.prose table').count()==5
        assert page.locator('.prose table').first.locator('a').count()==6
        assert page.locator('.prose details').count()==1
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Magazine overflow at {width}'
        prose=page.locator('.prose').text_content()
        assert 'Shared with Adam Abdelnaby' in prose and 'Shared with Selen Ceyran' in prose
        assert 'Table 12, case 4' in prose and 'Table 14, case 2' in prose
        assert 'MWTS' not in prose and 'three pilot locations' not in prose
        if width in [1440,390]:
            page.screenshot(path=str(dest/f'magazine-{width}.png'),full_page=True,animations='disabled')
            page.screenshot(path=str(dest/f'magazine-{width}-top.png'),animations='disabled')
        if width==390:
            page.locator('.mobile-toc summary').click()
            page.locator('.mobile-toc a').filter(has_text='My contribution').click()
            assert page.url.endswith('#my-contribution')
            assert not page.locator('.mobile-toc').get_attribute('open')
            page.locator('.prose table').first.get_by_role('link',name='Linear actuator mechanism',exact=True).click()
            assert page.url.endswith('#linear-actuator-mechanism')
            assert page.locator('#linear-actuator-mechanism').is_visible()
    for detail in page.locator('.prose details').all():
        detail.locator('summary').click()
        assert detail.locator('img').is_visible()
        detail.locator('.image-zoom').click()
        assert page.locator('dialog').is_visible()
        page.keyboard.press('Escape')
        assert not page.locator('dialog').is_visible()
    expected=page.locator('.prose').text_content()
    page.goto(url+'page1.html')
    assert page.locator('.prose').text_content()==expected,'Legacy Magazine content differs'
    nojs=page.context.browser.new_context(java_script_enabled=False,viewport={'width':390,'height':1000})
    static=nojs.new_page()
    static.goto(url+'case-studies/magazine-system/index.html')
    assert static.locator('.prose h2').count()==9
    static.get_by_text('View the selected response',exact=True).click()
    assert static.locator('.prose details').last.locator('img').is_visible()
    assert static.evaluate('document.documentElement.scrollWidth <= innerWidth')
    nojs.close()


def main():
    dest=ROOT/'artifacts';dest.mkdir(exist_ok=True)
    technical,_,_=markdown(r'''## Technical typesetting

Inline modulus: \(E = \Delta\sigma / \Delta\epsilon\).

$$
\sigma = \frac{F}{A_0}
$$

| Parameter | Value | Unit |
| --- | --- | --- |
| Example input | 1 | N |

```python
print("Technical content preview")
```
''')
    (dest/'technical-preview.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Technical content check</title><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/vendor/katex/katex.min.css"><script defer src="../assets/vendor/katex/katex.min.js"></script><script defer src="../assets/math.js"></script><script defer src="../assets/site.js"></script><main class="shell prose" style="max-width:760px;padding-block:60px"><h1>Technical preview</h1>'+technical+'</main></html>',encoding='utf-8')
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
        def copyfile(self, source, outputfile):
            # Chrome cancels media requests after metadata or navigation.
            try:
                super().copyfile(source, outputfile)
            except (ConnectionResetError, BrokenPipeError):
                pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT.parent)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/portfolio/'
    errors=[];results=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
            context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1)
            page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
            if '--magazine-only' in sys.argv:
                check_magazine(page,url,dest)
                assert not errors,errors
                browser.close()
                print('Magazine checks passed: 4 viewports, contribution table, figures, optional details, mobile TOC, legacy page and no-JavaScript reading.')
                return
            if '--gyroid-only' in sys.argv:
                check_gyroid(page,url,dest)
                assert not errors,errors
                browser.close()
                print('Gyroid checks passed: 4 viewports, figures, equations, tables, mobile TOC, image zoom and video playback.')
                return
            if '--home-only' in sys.argv:
                for width,name in [(1440,'desktop'),(768,'tablet'),(390,'mobile')]:
                    page.set_viewport_size({'width':width,'height':1000})
                    page.goto(url+'index.html')
                    page.locator('img[src]').evaluate_all('(images) => images.forEach(i => i.loading = "eager")')
                    page.evaluate('async () => Promise.all([...document.querySelectorAll("img[src]")].map(i => i.decode()))')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Home overflow at {width}'
                    page.screenshot(path=str(dest/f'home-{name}.png'),full_page=True,animations='disabled')
                page.locator('.capability').nth(1).click()
                assert page.locator('[data-project]:visible').count()>0
                assert not errors,errors
                browser.close()
                print('Homepage screenshots and approach link checked at 1440, 768 and 390px.')
                return
            for route in ['index.html','work.html','about.html','contact.html','page1.html','page2.html','page3.html','page4.html','page5.html','case-studies/magazine-system/index.html']:
                page.goto(url+route);page.wait_for_load_state('networkidle')
                page.locator('img[src]').evaluate_all('(images) => images.forEach(i => i.loading = "eager")')
                page.wait_for_function('[...document.querySelectorAll("img[src]")].every(i => i.complete && i.naturalWidth > 0)')
                assert page.locator('h1').count()==1,route
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow: {route}'
                assert page.locator('img[src]').evaluate_all('(images) => images.every(i => i.complete && i.naturalWidth > 0)'),f'Broken image: {route}'
                results.append(route)
            page.goto(url+'index.html');page.screenshot(path=str(dest/'home-desktop.png'),full_page=True)
            assert page.locator('.explore-card').count()==2
            assert page.locator('.explore-number').all_text_contents()==['04','05']
            featured_links=page.locator('.hero-project a.hero-art').evaluate_all('(links) => links.map(a => a.href)')
            extra_links=page.locator('.explore-card > a').evaluate_all('(links) => links.map(a => a.href)')
            assert not set(featured_links).intersection(extra_links),'Homepage repeats featured studies'
            page.get_by_role('tab').nth(1).focus();page.keyboard.press('ArrowRight')
            assert page.get_by_role('tab').nth(2).get_attribute('aria-selected')=='true'
            page.emulate_media(reduced_motion='reduce')
            page.get_by_role('tab').first.click()
            assert page.locator('.hero-project:visible').evaluate('(el) => getComputedStyle(el).animationName')=='none'
            page.emulate_media(reduced_motion='no-preference')
            page.goto(url+'work.html');page.get_by_role('button',name='Mechatronics',exact=True).click()
            assert page.locator('[data-project]:visible').count()==3
            page.get_by_role('searchbox').fill('Arduino')
            assert page.locator('[data-project]:visible').count()==2
            page.goto(url+'work.html');page.get_by_role('button',name='Robotics',exact=True).click()
            assert page.locator('[data-project]:visible').count()==2
            page.get_by_role('searchbox').fill('Arduino')
            assert page.locator('[data-project]:visible').count()==2
            page.get_by_role('searchbox').fill('no-such-project')
            assert page.locator('.empty-state').is_visible()
            page.get_by_role('button',name='Clear search and filters').click()
            assert page.locator('[data-project]:visible').count()==5
            page.goto(url+'work.html?discipline=Manufacturing&q=CFD')
            assert page.locator('[data-project]:visible').count()==1
            page.goto(url+'case-studies/magazine-system/index.html')
            page.locator('img[src]').evaluate_all('(images) => images.forEach(i => i.loading = "eager")')
            page.wait_for_function('[...document.querySelectorAll("img[src]")].every(i => i.complete && i.naturalWidth > 0)')
            page.locator('.image-zoom').first.click();assert page.locator('dialog').is_visible()
            page.keyboard.press('Escape');assert not page.locator('dialog').is_visible()
            page.evaluate('async () => { await Promise.all([...document.querySelectorAll("img[src]")].map(i => i.decode())); window.scrollTo(0,0); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }')
            page.screenshot(path=str(dest/'case-desktop-top.png'))
            page.screenshot(path=str(dest/'case-desktop.png'),full_page=True)
            for width in [390,320,768]:
                page.set_viewport_size({'width':width,'height':844})
                for route in ['index.html','work.html','about.html','contact.html','case-studies/magazine-system/index.html','case-studies/gyroid-structures/index.html']:
                    page.goto(url+route)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'{width}px overflow: {route}'
                if width==390:
                    page.goto(url+'index.html');page.get_by_role('button',name='Menu').click()
                    assert page.get_by_role('link',name='Work',exact=True).is_visible()
                    page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
                    page.locator('.menu-toggle').evaluate('(el) => el.blur()')
                    page.screenshot(path=str(dest/'home-mobile.png'),full_page=True)
                    page.goto(url+'case-studies/magazine-system/index.html');page.locator('.mobile-toc summary').click()
                    page.locator('.mobile-toc a').nth(1).click();assert not page.locator('.mobile-toc').get_attribute('open')
            page.goto(url+'artifacts/technical-preview.html');page.wait_for_load_state('networkidle')
            assert page.locator('.katex').count()==2,'Equations did not render'
            assert page.locator('math').count()==2,'Accessible MathML is missing'
            assert page.locator('.katex-error').count()==0
            assert page.locator('.table-scroll').count()==1
            assert page.get_by_role('button',name='Copy code').is_visible()
            for width in [390,320,1440]:
                page.set_viewport_size({'width':width,'height':900})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Technical content overflow: {width}'
                if width==320:page.screenshot(path=str(dest/'technical-mobile.png'),full_page=True)
            page.screenshot(path=str(dest/'technical-preview.png'),full_page=True)
            nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
            static=nojs.new_page();static.goto(url+'work.html')
            assert static.locator('[data-project]:visible').count()==5
            assert static.get_by_role('link',name='Contact',exact=True).is_visible()
            assert static.evaluate('document.documentElement.scrollWidth <= innerWidth'),'No-JS overflow'
            static.goto(url+'case-studies/gyroid-structures/index.html')
            assert static.locator('.prose h2').count()==7
            assert static.locator('.prose table').count()==4
            check_gyroid(page,url,dest)
            browser.close()
    finally:server.shutdown()
    assert not errors,'\n'.join(errors)
    (dest/'browser-check.json').write_text(json.dumps({'routes':results,'viewports':[1440,768,390,320],'errors':errors,'checks':['navigation','search','filters','empty state','shared filter URL','hero keyboard tabs','image dialog','mobile menu','mobile TOC','no-JavaScript reading']},indent=2),encoding='utf-8')
    print('Browser checks passed. Screenshots saved in artifacts/.')
if __name__=='__main__':main()
