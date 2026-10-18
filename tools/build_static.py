#!/usr/bin/env python3
"""重新生成静态HTML与示意地图。平时改页面不必运行；仅使用Python标准库。"""
from pathlib import Path
import html
import math
import re
from presentation_v2 import administrative_background, enrich_html

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
SPEC = ROOT / 'docs' / '内容与开发任务书.md'

NODES = [
    ('yudu','于都',115.42,25.95,'march',0,'P1',10,22,False),
    ('xiangjiang','湘江战役区域',111.07,25.93,'march',1,'P1',-105,30,True),
    ('zunyi','遵义',106.93,27.73,'march',2,'P1',12,22,False),
    ('chishui-region','赤水河流域',106,28.10,'march',3,'P2',-108,-8,True),
    ('jinshajiang','金沙江',102.42,26.30,'march',4,'P2',-13,30,True),
    ('luding','泸定',102.23,29.91,'march',5,'P2',-42,-15,False),
    ('snow-region','雪山区域',102.70,30.90,'march',6,'P2',12,2,True),
    ('grass-region','草地区域',103,32.70,'march',7,'P2',12,7,True),
    ('hadapu','哈达铺',104.22,34.20,'march',8,'P3',-70,-10,True),
    ('wuqi','吴起',108.18,36.93,'march',9,'P3',12,-14,False),
    ('shanghai','上海',121.47,31.23,'west',0,'P5',-3,32,False),
    ('nanjing','南京',118.80,32.06,'west',1,'P5',8,28,False),
    ('xuzhou-guide','',117.28,34.21,'west',2,'P5',0,0,True),
    ('zhengzhou-guide','',113.63,34.75,'west',3,'P5',0,0,True),
    ('tongguan','潼关',110.25,34.54,'west',4,'P5',-10,29,True),
    ('xian','西安',108.94,34.34,'west',5,'P6',-45,27,False),
]

def project(lon,lat):
    c=math.cos(math.radians(31.5))
    scale=min(880/(23*c),680/15)
    return ((1000-23*c*scale)/2+(lon-100)*c*scale,
            (800-15*scale)/2+(39-lat)*scale)

def point(node):
    x,y=project(node[2],node[3]); return f'{x:.1f},{y:.1f}'

def make_map(inline=False):
    attrs = 'id="route-map" class="route-map" data-mode="overview"' if inline else ''
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 800" {attrs} role="group" aria-label="中央红军长征及交大西迁主要节点示意图">',
      '<title>从长征路到西迁路</title><desc>两条路线分别通向陕北吴起与西安，背景为省级行政区划。</desc>']
    if not inline:
        parts.append('''<style>.map-grid{fill:none;stroke:#d8d0c2;stroke-dasharray:2 7}.grid-label{fill:#898073;font:12px sans-serif}.route-base{fill:none;stroke:#d5ccc0;stroke-width:2}.route-segment{fill:none;stroke-width:3.7;stroke-linecap:round;stroke-linejoin:round}.march{stroke:#a72c31}.west{stroke:#94651e;stroke-dasharray:9 7}.node-dot{fill:#f6f2e9;stroke:#a72c31;stroke-width:2.5}.node.west .node-dot{stroke:#94651e}.node-label{fill:#282724;stroke:#f6f2e9;stroke-width:5;paint-order:stroke;font:17px sans-serif}.touch-target,.node-ring{fill:none;stroke:none}.huining-label{fill:#696458;font:14px sans-serif;paint-order:stroke;stroke:#f6f2e9;stroke-width:4}.map-north{font:18px serif;fill:#696458}</style>''')
    parts.append('<style>.province{fill:#eee7d9;stroke:#c9bdab;stroke-width:1.25;stroke-linejoin:round}.province-focus{fill:#e9ddcc}.province-label{font:22px sans-serif;letter-spacing:3px;fill:#9b8b75;opacity:.70;pointer-events:none}.admin-background{pointer-events:none}</style>')
    parts.append(administrative_background(project,inline))
    for lon in [100,105,110,115,120]:
        x,y=project(lon,39); _,b=project(lon,24)
        parts.append(f'<path class="map-grid" d="M{x:.1f},{y:.1f}V{b:.1f}"/><text class="grid-label" x="{x+4:.1f}" y="{b+25:.1f}">{lon}°E</text>')
    for lat in [25,30,35]:
        x,y=project(100,lat); r,_=project(123,lat)
        parts.append(f'<path class="map-grid" d="M{x:.1f},{y:.1f}H{r:.1f}"/><text class="grid-label" x="{r-30:.1f}" y="{y-8:.1f}">{lat}°N</text>')
    parts.append('<g transform="translate(885 100)"><path d="M0 50V10m-6 12 6-12 6 12" fill="none" stroke="#696458"/><text class="map-north" x="-6" y="0">N</text></g>')
    for group in ['march','west']:
        nodes=[n for n in NODES if n[4]==group]
        coords=' '.join(point(n) for n in nodes)
        parts.append(f'<polyline class="route-base" data-route="{group}" points="{coords}"/>')
        for a,b in zip(nodes,nodes[1:]):
            parts.append(f'<path class="route-segment {group} is-shown" data-route="{group}" data-segment="{b[5]}" d="M{point(a)}L{point(b)}"/>')
    for n in NODES:
        id,label,lon,lat,group,order,chapter,dx,dy,minor=n
        if not label: continue # 走向参照点不画成已核实停靠站
        x,y=project(lon,lat)
        detail=' data-detail="route"' if id=='zunyi' else ' data-detail="ferry"' if id=='nanjing' else ' data-detail="rooted"' if id=='xian' else ''
        tag='a' if inline else 'g'
        link=f' href="#{chapter}" tabindex="0" aria-label="{html.escape(label)}，查看相关内容"' if inline else ''
        parts.append(f'<{tag}{link} class="node {group} is-visible {"minor" if minor else ""}" data-node="{id}" data-group="{group}" data-order="{order}"{detail}><title>{html.escape(label)}</title>')
        parts.append(f'<circle class="touch-target" cx="{x:.1f}" cy="{y:.1f}" r="25"/><circle class="node-ring" cx="{x:.1f}" cy="{y:.1f}" r="15"/>')
        if group=='west': parts.append(f'<rect class="node-dot" x="{x-5:.1f}" y="{y-5:.1f}" width="10" height="10"/>')
        else: parts.append(f'<circle class="node-dot" cx="{x:.1f}" cy="{y:.1f}" r="5"/>')
        parts.append(f'<text class="node-label" x="{x+dx:.1f}" y="{y+dy:.1f}">{html.escape(label)}</text></{tag}>')
    x,y=project(105.05,35.69)
    parts.append(f'<g data-huining="true" class="huining-marker is-visible"><path d="M{x-5:.1f},{y:.1f}l5-5 5 5-5 5Z" fill="#696458"/><text class="huining-label" x="{x-110:.1f}" y="{y-16:.1f}">1936 · 会师区域</text><text class="huining-label" x="{x-110:.1f}" y="{y+4:.1f}">会宁等地（另示）</text></g>')
    parts.append('</svg>')
    return '\n'.join(parts)

def prose(text):
    value=html.escape(text)
    def cite(match):
        ids=re.findall(r'S\d+',match.group())
        return ''.join(f'<sup><a class="ref" href="#source-{id}" data-source="{id}" aria-label="查看来源{id}">[{id[1:]}]</a></sup>' for id in ids)
    return re.sub(r'\[S\d+(?:、S\d+)*\]',cite,value)

def main():
    text=SPEC.read_text()
    chapters=[]
    for i in range(8):
        chunk=re.search(rf'### P{i}｜(.*?)(?=\n### P\d｜|\n## 3\.)',text,re.S).group(1)
        title=chunk.splitlines()[0]
        body=chunk.split('**正文：**',1)[1].split('\n**',1)[0].strip()
        time=re.search(r'\*\*时间：(.*?)\*\*',chunk)
        paragraphs=[x.strip() for x in body.split('\n\n') if x.strip()]
        chapters.append({'title':title,'period':time.group(1) if time else '', 'body':paragraphs})
    source_data=re.findall(r"\{id:'(S\d+)', title:'([^']+)', publisher:'([^']+)', url:'([^']+)', note:'([^']+)'\}", (SITE/'data.js').read_text())
    source_html=''.join(f'<div class="source-item" id="source-{id}"><a href="{url}" target="_blank" rel="noopener noreferrer">{id} · {title}</a><p>{publisher}。{note}</p></div>' for id,title,publisher,url,note in source_data)
    nav=''.join(f'<a href="#P{i}" data-nav="P{i}">{label}</a>' for i,label in [(1,'长征'),(4,'西迁'),(7,'接续')])
    extras={
      1:'<a class="detail-trigger" href="#sources" data-detail="route"><span class="detail-icon">阅</span><span><small>史料札记 01</small><strong>为什么路线会改变？</strong></span><span class="arrow">↗</span></a>',
      2:'<p class="chapter-rule">路线变化 ≠ 信念动摇</p>',
      3:'<p class="chapter-note">本图以中央红军长征主要节点为叙事线索；1936年会师另作补充标示。</p>',
      5:'<a class="detail-trigger" href="#sources" data-detail="ferry"><span class="detail-icon">渡</span><span><small>史料札记 02</small><strong>南京：火车也要坐船过江</strong></span><span class="arrow">↗</span></a>',
      6:'<div class="date-ticket"><div class="date">1956.09.10</div><p>迁校后的首次开学典礼<br>西安人民大厦礼堂</p><small>原创文字排版 · 史实依据 S8 · 非档案票证</small></div><a class="detail-trigger" href="#sources" data-detail="rooted"><span class="detail-icon">根</span><span><small>人物回忆</small><strong>从一趟列车，到一生扎根</strong></span><span class="arrow">↗</span></a><div class="rooted-steps">迁移<i></i>办学<i></i>扎根</div>'
    }
    content=''
    for i in range(1,7):
        c=chapters[i]; tone='west' if i>=4 else 'march'
        content+=f'''<section id="P{i}" class="chapter" data-chapter="true" data-tone="{tone}" aria-labelledby="title-P{i}"><div class="chapter-index {tone}">{i:02d} / {'西迁' if i>=4 else '长征'}</div><h2 id="title-P{i}">{c['title']}</h2><p class="chapter-period">{c['period']}</p><div class="chapter-body">{''.join('<p>'+prose(p)+'</p>' for p in c['body'])}</div>{extras.get(i,'')}</section>'''
    intro=''.join('<p>'+prose(p)+'</p>' for p in chapters[0]['body'])
    ending=''.join('<p>'+prose(p)+'</p>' for p in chapters[7]['body'])
    page=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f6f2e9"><meta name="description" content="沿中央红军长征与交大西迁的主要节点，重访两次出发，理解不同年代中的信念、选择与担当。"><meta property="og:title" content="山河为证——从长征路到西迁路"><meta property="og:description" content="长征胜利90周年 · 交大西迁70周年"><title>山河为证——从长征路到西迁路</title><link rel="icon" type="image/svg+xml" href="./assets/favicon.svg"><link rel="preload" href="./assets/fonts/shanhe-serif-subset.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="./styles.css"><script type="module" src="./app.js"></script></head>
<body><a class="skip-link" href="#P1">跳至正文</a><header class="topbar"><a class="brand" href="#P0"><span class="seal" aria-hidden="true">山</span>山河为证</a><nav aria-label="主要章节">{nav}<a href="#sources" data-source="">史料与来源</a></nav><button class="menu-button" data-open-toc aria-label="打开章节目录">目录 ☰</button><div class="progress-track" aria-hidden="true"><span id="reading-progress"></span></div></header>
<main><section class="hero" id="P0" data-chapter="true" aria-labelledby="hero-title"><div class="hero-art" aria-hidden="true"><img src="./assets/route-overview.svg" alt="" width="1000" height="800"></div><div class="hero-copy"><div class="hero-rule"></div><p class="eyebrow">长征胜利90周年 · 交大西迁70周年</p><h1 id="hero-title">山河为证</h1><p class="hero-subtitle">从长征路到西迁路</p><div class="hero-intro">{intro}</div><a class="start-link" href="#P1">沿路阅读<span aria-hidden="true">↓</span></a><div class="hero-meta"><span>1934—1936 / 长征</span><span>1956 / 西迁</span></div></div><div class="hero-side" aria-hidden="true">两次出发　山河之间</div><div class="hero-bottom">红色初心 · 长征礼赞　/　路线叙事作品</div></section>
<div class="journey"><aside class="map-panel" aria-label="随章节变化的路线图"><div class="map-heading"><div><p id="map-period">山河之间 · 两次出发</p><div id="map-chapter-title">两次出发</div></div><span class="map-number" id="map-index" aria-hidden="true">00</span></div><div class="map-window">{make_map(True)}</div><div class="map-notes"><div class="map-legend"><span><i class="legend-line"></i>中央红军长征</span><span><i class="legend-line west"></i>交大西迁</span></div><a href="#map-description" data-detail="geography">读图说明 ↗</a></div><p class="map-caption">按近似地理坐标绘制的主要节点示意，无行政底图；连接线不代表精确行军轨迹或历史铁路。吴起与西安分别为两条路线终点。</p><div class="map-foot"><span>主要节点 · 坐标示意</span><span>点击节点，查看内容</span></div></aside><div class="narrative">{content}</div></div>
<section class="outro" id="P7" data-chapter="true" aria-labelledby="outro-title"><div class="outro-layout"><div class="outro-copy"><p class="eyebrow">07 / 接续</p><h2 id="outro-title">今天，我们怎样继续</h2>{ending}<p class="outro-quote">山河见证来路，<br>行动写下接续。</p><div class="outro-actions"><a class="button-solid" href="#P1">重看两条路线 ↑</a><a href="#sources" data-source="">史料与素材来源 ↗</a></div></div><div class="outro-map-wrap"><img class="outro-map" src="./assets/route-overview.svg" width="1000" height="800" loading="lazy" alt="两条路线分别抵达陕北吴起与西安，空间位置及连线为主要节点示意"><p class="outro-map-caption">不同的终点，相通的担当。主要节点示意，非精确历史轨迹。</p></div></div></section>
<section class="sources-section" id="sources" aria-label="史料与素材来源"><details open><summary>史料与素材来源</summary><div class="source-grid">{source_html}</div><p class="source-credit" id="map-description">地图说明：本版采用近似坐标示意，无行政边界或地形底图。长征以中央红军主要节点为线索，1936年会师另示；西迁连接线仅表示大致走向。图形与轮渡示意为原创，非历史现场复原。</p><p class="source-credit">字体：Shanhe Serif，为Noto Serif CJK SC Regular的字符子集，遵循SIL Open Font License 1.1。本版未使用第三方历史照片。正文为据上述资料的原创改写；资料核对日期：2026年10月18日。</p></details></section></main>
<footer class="footer"><p>山河为证 · 从长征路到西迁路</p><p id="author-line">红色初心 · 长征礼赞 / 2026</p></footer><dialog class="reader-dialog" id="reader-dialog" aria-labelledby="dialog-title"><div class="dialog-header"><h2 id="dialog-title">史料札记</h2><button class="dialog-close" data-close-dialog aria-label="关闭面板">×</button></div><div class="dialog-body" id="dialog-body"></div></dialog><noscript><style>.map-panel{{position:relative;top:0;height:auto;min-height:0}}.route-map{{max-height:none}}.journey{{display:block}}.chapter{{min-height:0}}.detail-trigger{{display:none}}</style></noscript></body></html>'''
    page=enrich_html(page)
    SITE.mkdir(exist_ok=True)
    (SITE/'index.html').write_text(page)
    (SITE/'assets'/'route-overview.svg').write_text(make_map())
    print('Generated site/index.html and site/assets/route-overview.svg')

if __name__=='__main__': main()
