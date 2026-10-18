#!/usr/bin/env python3
"""可选：用Ma Shan Zheng完整TTF重建标题字体，需fonttools及brotli。"""
from pathlib import Path
import argparse

def main():
    from fontTools import subset
    from fontTools.ttLib import TTFont
    p=argparse.ArgumentParser();p.add_argument('font',type=Path);args=p.parse_args()
    root=Path(__file__).resolve().parents[1]
    text='山河为证从长征路到西迁信念担当奋斗'+''.join(chr(i) for i in range(32,127))
    opts=subset.Options();opts.flavor='woff2';opts.layout_features=['*']
    font=TTFont(args.font);s=subset.Subsetter(options=opts);s.populate(text=text);s.subset(font)
    for n in font['name'].names:
        if n.nameID in {1,4,6,16,17}:
            name={1:'Shanhe Brush',4:'Shanhe Brush Regular',6:'ShanheBrush-Regular',16:'Shanhe Brush',17:'Regular'}[n.nameID]
            n.string=name.encode(n.getEncoding())
    font.flavor='woff2';out=root/'site/assets/fonts/shanhe-brush-subset.woff2';font.save(out)
    print(out.name,out.stat().st_size)

if __name__=='__main__':main()
