import pymongo
import http.client
import hashlib
import urllib
import random
import json
import time
import os


with open('Spider/config_local.json', 'r', encoding='utf8') as f:
    config_local = json.load(f)
    appid = config_local['tr_appid']
    secretKey = config_local['tr_secretKey']
    mongo_port = config_local['mongo_port']
my_tr_url = '/api/trans/vip/fieldtranslate'
fromLang, toLang = 'en', 'zh'


def translate(query):
    time.sleep(1)
    salt = random.randint(32768, 65536)
    domain = 'medicine'  # 医疗领域
    # 签名
    sign = f'{appid}{query}{salt}{domain}{secretKey}'
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = (f'{my_tr_url}?appid={appid}&q='
           f'{urllib.parse.quote(query)}&from={fromLang}'
           f'&to={toLang}&salt={salt}&domain={domain}&sign={sign}')
    try:
        httpClient = http.client.HTTPConnection(
            'api.fanyi.baidu.com')
        httpClient.request('GET', url)
        res = httpClient.getresponse()
        result = res.read().decode('unicode_escape')
        return json.loads(result)
    except Exception as e:
        return {'trans_result': None, 'error_info': str(e)}


class SpiderPipeline(object):
    client = pymongo.MongoClient('localhost', mongo_port)
    db = client['cns']

    def process_item(self, item, spider):
        # 处理数据并验证有效性
        sheet = self.db[item['journal']]
        res = sheet.find_one(
            {'volume': item['volume'], 'title': item['title']})
        if res is None or len(res) <= 0:
            title_zh = translate(item['title'])
            if title_zh['trans_result'] is not None:
                t_zh = ''
                for tr in title_zh['trans_result']:
                    t_zh = t_zh + tr['dst']
                title_zh = t_zh
            else:
                self.db['error'].insert(
                    {"info": title_zh['error_info'], 'data': item['title']})
                title_zh = item['title']

            if item['summary']:
                summary_zh = translate(item['summary'])
            else:
                summary_zh = {'trans_result': [{'dst': ''}]}
            if summary_zh['trans_result'] is not None:
                s_zh = ''
                for tr in summary_zh['trans_result']:
                    s_zh = s_zh + tr['dst']
                summary_zh = s_zh
            else:
                self.db['error'].insert(
                    {"info": summary_zh['error_info'], 'data': item['title']})
                summary_zh = item['summary']

            sheet.insert_one({
                'volume': item['volume'], 'title': item['title'],
                'url': item['url'], 'chapter': item['chapter'],
                'summary': item['summary'], 'state': 'unsent',
                'title_zh': title_zh, 'summary_zh': summary_zh})

        return item
