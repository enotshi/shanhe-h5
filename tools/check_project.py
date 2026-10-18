#!/usr/bin/env python3
"""零依赖文件检查；不代替浏览器视觉与实机测试。"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
errors=[]

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.links=[]; self.refs=[]; self.text=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        for k in ['src','href']:
            if k in a: self.refs.append((tag,k,a[k]))
        if tag=='img' and 'alt' not in a: errors.append('Image lacks alt')
    def handle_data(self,data): self.text.append(data)

doc=Document(); doc.feed((SITE/'index.html').read_text())
if len(doc.ids)!=len(set(doc.ids)): errors.append('Duplicate HTML IDs')
for i in range(8):
    if f'P{i}' not in doc.ids: errors.append(f'Missing chapter P{i}')
for tag,key,ref in doc.refs:
    if ref.startswith('#'):
        if ref[1:] and ref[1:] not in doc.ids: errors.append(f'Broken anchor {ref}')
    elif not urlsplit(ref).scheme:
        path=(SITE/unquote(urlsplit(ref).path)).resolve()
        if not path.is_file(): errors.append(f'Missing local resource {ref}')
        if ref.startswith('/'): errors.append(f'Root absolute path breaks project Pages: {ref}')
    elif key=='src': errors.append(f'Unexpected external runtime resource {ref}')
for file in SITE.glob('*.js'):
    for dep in re.findall(r"(?:from\s+|import\s*)['\"]([^'\"]+)['\"]",file.read_text()):
        if not (file.parent/dep).is_file(): errors.append(f'Broken module {dep}')
for file in (SITE/'assets').glob('*.svg'):
    try: ET.parse(file)
    except ET.ParseError as e: errors.append(f'Invalid SVG {file}: {e}')
css=(SITE/'styles.css').read_text()
for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)',css):
    if not (SITE/ref).is_file(): errors.append(f'Missing CSS asset {ref}')
for needed in ['.github/workflows/pages.yml','README.md','THIRD_PARTY_NOTICES.md','site/assets/fonts/OFL.txt']:
    if not (ROOT/needed).is_file(): errors.append(f'Missing deliverable {needed}')
font=SITE/'assets/fonts/shanhe-serif-subset.woff2'
if not font.is_file() or font.read_bytes()[:4]!=b'wOF2': errors.append('Invalid/missing WOFF2 font')
if font.is_file() and font.stat().st_size>1500000: errors.append('Font subset unexpectedly large')
size=sum(p.stat().st_size for p in SITE.rglob('*') if p.is_file())
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: 8 chapters; {len(doc.ids)} unique IDs; local links/modules/SVG/font/licenses OK')
print(f'Static site: {size/1024:.1f} KiB. Browser rendering and live deployment are separate checks.')
