"""Tests for authoring features and draft publishing boundaries."""
import unittest,tempfile,re,yaml
from pathlib import Path
from unittest.mock import patch
import build

class ContentTests(unittest.TestCase):
    def test_home_additional_studies_exclude_featured_and_grow(self):
        projects=build.load_projects()
        config=yaml.safe_load((build.ROOT/'content/site.yml').read_text(encoding='utf-8'))
        result=build.home(projects,config)
        featured={p['slug'] for p in projects if p['featured']}
        additional=re.findall(r'data-home-study="([^"]+)"',result)
        self.assertEqual(additional,['quadruped-robot','arduino-drone'])
        self.assertFalse(featured.intersection(additional))
        extra={**projects[-1],'slug':'new-study','short_title':'New study','url':'case-studies/new-study/index.html','order':6,'featured':False,'cover':''}
        expanded=build.home([*projects,extra],config)
        self.assertIn('data-home-study="new-study"',expanded)
        self.assertIn('class="explore-number">06</span>',expanded)

    def test_labels_keep_original_discipline(self):
        p={'discipline':'Robotics','tags':['Mechatronics','Robotics']}
        self.assertEqual(build.project_labels(p),['Robotics','Mechatronics'])

    def test_technical_content(self):
        source=r'''## Calculation

Inline \(E = \frac{\Delta\sigma}{\Delta\epsilon}\).

$$
\sigma = \frac{F}{A_0}
$$

| Input | Unit |
| --- | --- |
| Force | N |

```python
print("<result>")
```

## Calculation
Second calculation.
'''
        result,toc,math=build.markdown(source)
        self.assertTrue(math)
        self.assertIn(r'\frac{F}{A_0}',result)
        self.assertIn('data-display="true"',result)
        self.assertIn('<table>',result)
        self.assertIn('&lt;result&gt;',result)
        self.assertEqual([x[0] for x in toc],['calculation','calculation-2'])

    def test_missing_media_retained_but_not_broken_on_page(self):
        result,toc,_=build.markdown('## Project gallery\n\n![Sample](<images/absent-image.png> "Caption")',source='test')
        self.assertNotIn('<img',result)
        self.assertNotIn('Project gallery',result)
        self.assertEqual(toc,[])

    def test_captions_and_subdirectory_paths(self):
        result,_,_=build.markdown('![Assembly](images/magazine.png "Assembly overview")','../../')
        self.assertIn('src="../../images/magazine.png"',result)
        self.assertIn('<figcaption>Assembly overview</figcaption>',result)
        self.assertNotIn('<p><figure',result)

    def test_unclosed_math_fails_the_build(self):
        with self.assertRaises(ValueError):build.markdown('$$\nx = 1')

    def test_draft_is_not_loaded(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'draft.md'
            p.write_text('---\ntitle: Draft\nslug: draft\nsummary: Hidden\ndiscipline: Test\nrole: Author\ndraft: true\n---\nPrivate draft',encoding='utf-8')
            self.assertEqual(build.load_projects(Path(folder)),[])

    def test_duplicate_slug_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            body='---\ntitle: Example\nslug: same\nsummary: Example\ndiscipline: Test\nrole: Author\n---\nText'
            for name in ['one','two']:(Path(folder)/(name+'.md')).write_text(body,encoding='utf-8')
            with self.assertRaises(ValueError):build.load_projects(Path(folder))

    def test_obsolete_generated_pages_are_removed(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder); original=build.load_projects()
            with patch.object(build,'load_projects',return_value=original):build.build(out)
            target=out/original[0]['url'];self.assertTrue(target.exists())
            with patch.object(build,'load_projects',return_value=original[1:]):build.build(out)
            self.assertFalse(target.exists())
            self.assertFalse((out/original[0]['legacy']).exists())

if __name__=='__main__':unittest.main()
