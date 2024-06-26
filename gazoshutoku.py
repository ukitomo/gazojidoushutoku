#!/usr/bin/python
#coding=utf-8
import sys
import time
from datetime import datetime
import os
import requests
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

#接続
url = None
while not url:
    url = input("URLを入力してください")
print(url)
if not (url.startswith('https://') or url.startswith('http://')):
    url = "http://" + url
try:
    res = requests.get(url)
except requests.exceptions.ConnectionError:
    print("接続に失敗しました")
    sys.exit(1)
if res.status_code != requests.codes.ok:
    print("接続に失敗しました")
    sys.exit(1)
#セレクター指定
selecter = None
while not selecter:
   selecter = input("CSSセレクターを入力してください")
print(selecter)
soup = BeautifulSoup(res.text, 'html.parser')
pictures = soup.select(selecter)
if pictures:
    for pictureslist in pictures:
        print(pictureslist)    
    answer = input("これらの要素が" + str(len(pictures)) + "個見つかりましたダウンロードしますか?(y/n)")
else:
    print("要素が見つかりませんでした")
    sys.exit(1)
if answer == "y":
    #フォルダ作成
    dt = datetime.now()
    datetime_str = dt.strftime("%Y%m%d_%H%M%S")
    if not os.path.isdir('./image'):
        img_dir = Path('./image')
        img_dir.mkdir(exist_ok=True)
    if url.startswith('https://'):
        url_no_protocol = url.rstrip('/')
        url_no_protocol = url_no_protocol.removeprefix('https://')
    elif url.startswith('http://'):
        url_no_protocol = url.rstrip('/')
        url_no_protocol = url_no_protocol.removeprefix('http://')
    img_dir = Path('./image/' + url_no_protocol.replace('/', '-') + "(" + datetime_str + ")" ) 
    img_dir.mkdir(exist_ok=True)
    #画像取得
    for picture in pictures:
        try:
            url_rel = picture['src']
        except KeyError:
            print("src属性がありません")
            time.sleep(1)
            continue
        url_abs = urljoin(url, url_rel)
        print(url_abs)
        try:
            img_res = requests.get(url_abs)
        except requests.exceptions.ConnectionError:
            print("接続に失敗しました")
            time.sleep(1)
            continue                
        print(img_res)
        if img_res.status_code != requests.codes.ok:
            print("ダウンロードに失敗しました")
            time.sleep(1)
            continue
        img_name = Path(url_abs).name
        img_file_path = img_dir / img_name
        img_file_path.write_bytes(img_res.content)
        print(img_name)     
        time.sleep(1)
print("プログラムは終了しました")