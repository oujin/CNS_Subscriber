import os
import schedule
import time
from sendemail import sendmail
import pymongo


def make_content(items):
    content = ''
    for item in items:
        content = f'{content}{"-" * 100}<br/>{"-" * 100}<br/>'
        content = f'{content}Title: {item["title"]}<br/>'
        content = f'{content}标题: {item["title_zh"]}<br/>'
        content = f'{content}Volume: {item["volume"]}<br/>'
        content = f'{content}Category: {item["chapter"]}<br/>'
        content = f'{content}Summary: {item["summary"]}<br/>'
        content = f'{content}摘要: {item["summary_zh"]}<br/>'
        content = f'{content}url: <a href="{item["url"]}">{item["url"]}</a>'
        content = f'{content}<br/>###<br/><br/>'
    content = (f'{content}<br/><br/>注：可能由于解析器的问题导致个别文章被遗漏，'
               f'更完整内容参看官网。翻译来自百度。<br/><br/>')
    return content


def send_news():
    # 遍历数据库
    client = pymongo.MongoClient('localhost', 29527)
    collection = ['cell', 'nature', 'natureMI',
                  'patterns', 'science']
    # collection = ['cell']
    db = client['cns']
    for col in collection:
        time.sleep(3)
        os.system(f'scrapy crawl {col} -s LOG_FILE=spider.log')
        res = db[col].find({"state": "unsent"}, {"volume": 1})
        volumes = set()
        for r in res:
            volumes.add(r['volume'])
        for volume in volumes:
            data = db[col].find({"state": "unsent", "volume": volume}
                                ).sort([('chapter', 1)])
            content = make_content(data)
            subject = f'《{col}》期刊 · {volume}'

            # 发送邮件
            users = db['yonghu'].find({})
            receivers = []
            for user in users:
                receivers.append(user['email'])
            try:
                sendmail(receivers, subject, content)
                # 更新
                db[col].update(
                    {"volume": volume}, {"$set": {"state": "sent"}},
                    multi=True)
            except Exception as e:
                db['error'].insert({"info": str(e), "data": "sending email"})


if __name__ == '__main__':
    send_news()
    schedule.every().day.at("21:00").do(send_news)
    while True:
        schedule.run_pending()
        time.sleep(60)
