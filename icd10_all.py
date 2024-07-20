import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://www.byomei.org/icd10/index.html'

# HTTP GETリクエストを送信してページの内容を取得する
response = requests.get(url)
# 2. エンコーディングを設定
response.encoding = 'shift_jis'  # 必要に応じて適切なエンコーディングを設定

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(response.text, 'html.parser')

# すべてのtrタグを取得
trs = soup.find_all('tr')

# すべてのリンクを格納するリスト
links = []

# 各trタグ内のリンクを取得
for tr in trs:
    a_tag = tr.find('a', href=True)
    if a_tag:
        if(a_tag['href'] != '../index.html'):
            links.append(a_tag['href'])
            

