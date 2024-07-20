import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

def scrape_icd_codes(url):
    try:
        # HTTP GETリクエストを送信してページの内容を取得する
        response = requests.get(url)
        # エンコーディングを設定
        response.encoding = 'shift_jis'  # 必要に応じて適切なエンコーディングを設定

        # BeautifulSoupを使用してHTMLを解析する
        soup = BeautifulSoup(response.text, 'html.parser')

        # ul要素の中の各li要素を取得し、ICD-10コードと名称を抽出する
        icd_codes = []
        for li in soup.select('li li'):
            code = li.find('font').text.strip()  # ICD-10コードを取得
            name = li.find('a').text.replace(code, '').strip()  # 名称を取得
            icd_codes.append((code, name))

        return icd_codes
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def save_to_csv(icd_codes, filename='icd10_AB_3桁.csv'):
    try:
        # データフレームに変換
        result_df = pd.DataFrame(icd_codes, columns=['ICD-10 Code', 'Name'])

        # CSVファイルに保存
        result_df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f"{filename} 作成成功")
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("urlが指定されていない")
    else:
        url = sys.argv[1]
        icd_codes = scrape_icd_codes(url)
        save_to_csv(icd_codes)
