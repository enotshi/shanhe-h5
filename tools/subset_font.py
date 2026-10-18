#!/usr/bin/env python3
"""可选字体重建。pip install 'fonttools[woff]' brotli 后，传入上游完整OTF路径。"""
from pathlib import Path
import argparse

def main():
    from fontTools import subset
    from fontTools.ttLib import TTFont
    parser=argparse.ArgumentParser()
    parser.add_argument('font',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    text=''.join(p.read_text() for p in (root/'site').rglob('*')
                 if p.is_file() and p.suffix in {'.html','.js','.css','.svg'})
    text+=''.join(chr(i) for i in range(32,127))
    opts=subset.Options(); opts.flavor='woff2'; opts.layout_features=['*']
    font=TTFont(args.font)
    engine=subset.Subsetter(options=opts); engine.populate(text=text); engine.subset(font)
    # 子集为修改字体，采用新名称，保留上游版权与OFL信息。
    for n in font['name'].names:
        if n.nameID in {1,4,6,16,17}:
            names={1:'Shanhe Serif',4:'Shanhe Serif Regular',6:'ShanheSerif-Regular',16:'Shanhe Serif',17:'Regular'}
            try: n.string=names[n.nameID].encode(n.getEncoding())
            except (UnicodeEncodeError,LookupError): n.string=names[n.nameID].encode('utf-16-be')
    if 'CFF ' in font:
        cff=font['CFF '].cff
        cff.fontNames=['ShanheSerif-Regular']
        for top in cff.topDictIndex:
            top.FullName='Shanhe Serif Regular'
            top.FamilyName='Shanhe Serif'
    font.flavor='woff2'
    out=root/'site/assets/fonts/shanhe-serif-subset.woff2'
    font.save(out)
    print(f'{out}: {out.stat().st_size} bytes')

if __name__=='__main__': main()
