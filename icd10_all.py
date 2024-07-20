import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import configparser

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
            icd_codes.append([code, name])

        return icd_codes
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def save_to_csv(icd_codes, filename='icd10_3.csv'):
    try:
        # データフレームに変換
        result_df = pd.DataFrame(icd_codes)
        # , columns=['ICD-10 Code', 'Name']

        # CSVファイルに保存
        result_df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f"{filename} 作成成功")
    except Exception as e:
        print(f"エラー: {e}")

def get_db_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    db_config = {
        'server': config.get('database', 'server'),
        'database': config.get('database', 'database')
    }
    return db_config

def save_to_sql_server(icd_codes, table_name, server, database):
    try:
        # データフレームに変換
        result_df = pd.DataFrame(icd_codes, columns=['icd_code_first3', 'name'])
        
        # SQL Serverへの接続エンジンを作成
        connection_string = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        engine = create_engine(connection_string)
        
        # データフレームをSQL Serverに保存
        result_df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        
        print(f"{table_name} テーブルにデータを保存しました")
    except Exception as e:
        print(f"エラー: {e}")

def get_all_url():
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
    return links

            
if __name__ == '__main__':
    links = get_all_url()
    icd_codes = []
    for link in links:
        url = 'http://www.byomei.org/icd10/'+link
        print(url)
        for icd in scrape_icd_codes(url):
            if(icd[1] != ''):# たまに例外で取得してしまうコード
                icd_codes.append(icd)

    save_to_csv(icd_codes)

    # データベース接続情報の取得
    db_config = get_db_config()
    save_to_sql_server(
        icd_codes,
        table_name='M_icd10_first3',
        server=db_config['server'],
        database=db_config['database']
    )


