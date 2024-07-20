import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://www.byomei.org/icd10/A00-B99.html'

# HTTP GETリクエストを送信してページの内容を取得する
response = requests.get(url)
# 2. エンコーディングを設定
response.encoding = 'shift_jis'  # 必要に応じて適切なエンコーディングを設定

# BeautifulSoupを使用してHTMLを解析する
soup = BeautifulSoup(response.text, 'html.parser')

# ul要素の中の各li要素を取得し、ICD-10コードと名称を抽出する
icd_codes = []
for li in soup.select('li li'):
    code = li.find('font').text.strip()  # ICD-10コードを取得
    name = li.find('a').text.replace(code, '').strip()  # 名称を取得
    icd_codes.append((code, name))

result_df = pd.DataFrame(icd_codes)

result_df.to_csv('icd10_AB_3桁.csv', index=False, encoding='utf-8-sig')