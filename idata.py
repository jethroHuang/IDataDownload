from requests import get
from iDataConfig import *

def search(keyword, db='SCDB', start=0):
    data = {
        'app_id': appid,
        'access_token': access_token,
        'keyword': keyword,
        'db': db,
        'sort_type': 1,
        'start': start
    }
    res = get('https://api.cn-ki.net/openapi/search', params=data)
    return res.json()


def get_detail(filename, dbcode):
    params = {
        'app_id': appid,
        'access_token': access_token,
        'filename': filename,
        'dbcode': dbcode
    }
    res = get('https://api.cn-ki.net/openapi/doc_detail', params=params)
    return res.json()


def get_durl(filename, filename_en, title, tablename):
    data = {
        'app_id': appid,
        'access_token': access_token,
        'filename': filename,
        'filename_en': filename_en,
        'title': title,
        'tablename': tablename
    }
    res = get('https://api.cn-ki.net//openapi/get_durl', params=data)
    return res.json()


if __name__ == "__main__":
    res = search("美国量化宽松货币政策的退出及其对中国经济的影响")
    for item in res['data']['items']:
        url = get_durl(item['filename'], item['filename_en'], item['title'], item['author'], item['tablename'])
        print('-' * 15)
        print(url)
