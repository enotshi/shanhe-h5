#!/usr/bin/env python3
"""可选：用最终HTTPS网址生成投稿二维码；pip install 'qrcode[pil]'。"""
from pathlib import Path
from urllib.parse import urlsplit
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('url',help='最终公开HTTPS网址')
    parser.add_argument('--output',default='output/作品二维码.png')
    args=parser.parse_args(); parsed=urlsplit(args.url)
    if parsed.scheme!='https' or not parsed.hostname or parsed.hostname in {'localhost','127.0.0.1','0.0.0.0'}:
        parser.error('请使用最终公开HTTPS网址，不要使用localhost或本地预览地址')
    import qrcode
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=16,border=4)
    qr.add_data(args.url);qr.make(fit=True);qr.make_image(fill_color='#282724',back_color='white').save(out)
    print(out.resolve())

if __name__=='__main__': main()
