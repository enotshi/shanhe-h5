"""v1.1的行政区背景与内容增强。只负责生成静态内容，不是网页运行依赖。"""
from pathlib import Path
import json
import html

ROOT=Path(__file__).resolve().parents[1]

def administrative_background(project,inline):
    data=json.loads((ROOT/'tools/data/provinces.json').read_text())
    # 局部图的显示范围与路线投影保持一致，完整源数据留在tools/data供追溯。
    clip='regional-admin-clip-inline' if inline else 'regional-admin-clip-image'
    parts=[f'<defs><clipPath id="{clip}"><rect x="58" y="60" width="884" height="680"/></clipPath></defs>',
           f'<g class="admin-background" clip-path="url(#{clip})" aria-hidden="true">']
    focus={'江西省','贵州省','四川省','云南省','甘肃省','陕西省','河南省','安徽省','江苏省','上海市'}
    for f in data['features']:
        name=f['properties'].get('name','')
        if not name: continue
        g=f['geometry']; polygons=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
        coords=[p for poly in polygons for ring in poly for p in ring]
        if not coords: continue
        xs=[p[0] for p in coords]; ys=[p[1] for p in coords]
        if max(xs)<100 or min(xs)>123 or max(ys)<24 or min(ys)>39: continue
        d=[]
        for poly in polygons:
            for ring in poly:
                pts=[project(*p[:2]) for p in ring]
                if not pts:continue
                d.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z')
        cls='province province-focus' if name in focus else 'province'
        parts.append(f'<path class="{cls}" data-province="{html.escape(name)}" fill-rule="evenodd" d="{"".join(d)}"/>')
    labels=[('陕西',109.6,35.6),('甘肃',102.2,35.7),('四川',104.2,30.6),('云南',101.0,25.0),
      ('贵州',106.8,26.5),('广西',108.8,24.5),('湖南',111.3,28.3),('江西',115.2,27.7),
      ('湖北',112.5,30.8),('河南',113.7,33.8),('江苏',119.4,33.7),('安徽',117.4,31.7),
      ('浙江',120.0,29.0),('福建',117.7,25.7),('山东',118.1,36.5),('山西',112.0,37.1),
      ('重庆',107.6,29.6),('宁夏',106.0,37.7)]
    for label,lon,lat in labels:
        x,y=project(lon,lat)
        parts.append(f'<text class="province-label" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{label}</text>')
    parts.append('</g>')
    return ''.join(parts)

def icon(name,cls='theme-icon'):
    return f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true"><use href="./assets/red-icons.svg#{name}"/></svg>'

def photo(id,file,title,caption,source,width,height,compact=False):
    return f'''<figure class="archive-photo {'archive-photo-compact' if compact else ''}"><a class="photo-open" href="./assets/photos/{file}" data-photo="{id}" aria-label="查看图片：{title}"><img src="./assets/photos/{file}" width="{width}" height="{height}" loading="lazy" decoding="async" alt="{title}"/><span class="photo-expand">查看影像 ↗</span></a><figcaption><strong>{title}</strong><span>{caption}</span><a href="{source}" target="_blank" rel="noopener noreferrer">来源原文 ↗</a></figcaption></figure>'''

def enrich_html(page):
    page=page.replace('<link rel="preload" href="./assets/fonts/shanhe-serif-subset.woff2"', '<link rel="preload" href="./assets/fonts/shanhe-brush-subset.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="./assets/fonts/shanhe-serif-subset.woff2"')
    page=page.replace('<div class="hero-rule"></div>',f'<div class="hero-rule"></div><div class="red-motif">{icon("flag")}<span>信念 · 担当 · 奋斗</span>{icon("star","motif-star")}</div>')
    page=page.replace('<div class="hero-side"', '<div class="hero-ribbon" aria-hidden="true"></div><div class="hero-side"')
    page=page.replace('01 / 长征</div>','01 / 长征'+icon('flag')+'</div>')
    page=page.replace('04 / 西迁</div>','04 / 西迁'+icon('train')+'</div>')
    page=page.replace('06 / 西迁</div>','06 / 西迁'+icon('book')+'</div>')
    page=page.replace('<p class="eyebrow">07 / 接续</p>',f'<p class="eyebrow ending-eyebrow">{icon("letter")}07 / 接续</p>')
    ticket=photo('ticket','ticket-1956.jpg','一张乘车证，一次西行','1956年9月2日乘车证｜西安交通大学西迁精神专题网','https://xq.xjtu.edu.cn/info/1022/2508.htm',1024,605)
    departure=photo('departure','departure-1956.jpeg','从徐家汇启程','1956年8月欢送赴陕师生｜西安交大“西迁记忆”','https://xqjy.xjtu.edu.cn/info/1063/1245.htm',252,236,True)
    opening=photo('opening','opening-1956.jpg','课堂在西安继续','1956年迁校后首次开学典礼｜西安交大“西迁记忆”','https://xqjy.xjtu.edu.cn/info/1063/1246.htm',382,276)
    walk=photo('walk','walk-2026.png','把来路走成新的出发','2026年“重走长征路 奋进新征程”活动报道配图｜图片：校工会','https://news.xjtu.edu.cn/info/1007/230870.htm',1267,476)
    marker='<a class="detail-trigger" href="#sources" data-detail="ferry">'
    page=page.replace(marker,f'<div class="archive-pair">{ticket}{departure}</div>'+marker)
    page=page.replace('<div class="date-ticket">',opening+'<div class="date-ticket">')
    page=page.replace('原创文字排版 · 史实依据 S8 · 非档案票证','迁校后的首次开学典礼')
    # 移出技术措辞，保留清晰、必要的历史终点关系。
    old='按近似地理坐标绘制的主要节点示意，无行政底图；连接线不代表精确行军轨迹或历史铁路。吴起与西安分别为两条路线终点。'
    page=page.replace(old,'从于都到陕北，从上海到西安。沿着两条道路，重访时代的选择。')
    page=page.replace('读图说明 ↗','两条道路 ↗').replace('主要节点 · 坐标示意','行经山河 · 路线总览')
    page=page.replace('不同的终点，相通的担当。主要节点示意，非精确历史轨迹。','不同的终点，相通的担当。')
    page=page.replace('两条路线分别抵达陕北吴起与西安，空间位置及连线为主要节点示意','两条路线分别抵达陕北吴起与西安，背景为省级行政区划')
    start='<p class="source-credit" id="map-description">'
    end='</p></details></section></main>'
    a=page.index(start);b=page.index(end,a)+len('</p>')
    page=page[:a]+'<p class="source-credit" id="map-description">图文出处见各图图注及以上史料条目。</p>'+page[b:]
    # 替换第七部分为回信与当代行动，引用严格区分原文与作者阐释。
    a=page.index('<h2 id="outro-title">');b=page.index('<p class="outro-quote">',a)
    ending=f'''<h2 id="outro-title">把精神写进今天的行动</h2>
<p>长征与西迁，是不同年代对时代任务的回答。走到今天，传承也需要找到具体的着力点。</p>
<div class="letter-card"><div class="letter-date">2026 · 04 · 07</div><p class="letter-context">习近平给四所交通大学全体师生回信</p><blockquote>“传承弘扬西迁精神，聚焦国家重大战略需求”</blockquote><a href="https://www.xinhuanet.com/politics/20260407/93ffd51c2a1449ebb82f84235b005ab1/c.html" target="_blank" rel="noopener noreferrer">回信原文 ↗</a><a class="ref" href="#source-S9" data-source="S9" aria-label="查看回信来源">[9]</a></div>
<p>这封回信写给上海交通大学、西安交通大学、西南交通大学、北京交通大学全体师生，并对科技创新、人才培养和产学研融合提出期望。</p>
<p>对今天的我们而言，接续可以落实为一次严谨的实验、一项回应真实需求的研究、一段深入现场的实践。既把学问做扎实，也不断追问：自己的知识和行动，能够为国家与社会解决什么问题？</p>
<div class="practice-links"><span>{icon('book')}求知以致用</span><span>{icon('star')}担当见行动</span></div>
'''
    page=page[:a]+ending+page[b:]
    # 将当代报道置于尾声之后，不挤进地图与正文的窄栏。
    before='<section class="sources-section"'
    news=f'''<section class="news-bridge" aria-labelledby="news-title"><div class="news-copy"><p class="eyebrow">从纪念到行动</p><h2 id="news-title">让两种精神<br>走进共同的脚步</h2><p>2026年4月，西安交大启动“重走长征路 奋进新征程”教职工健步走活动，将长征精神与西迁精神的传承融入校园生活。</p><a href="https://news.xjtu.edu.cn/info/1007/230870.htm" target="_blank" rel="noopener noreferrer">阅读校园报道 ↗</a></div>{walk}</section>'''
    page=page.replace(before,news+before)
    return page
