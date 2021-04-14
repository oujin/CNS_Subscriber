import scrapy
from Spider.items import ArticleItem
import os
import time


class CellSpider(scrapy.Spider):
    name = "cell"
    allowed_domains = ['sciencedirect.com']
    start_urls = [
        'https://www.sciencedirect.com/journal/cell'
    ]

    def abstract_parse(self, response):
        res = response.xpath('//*[@class="Article"]')
        chapter = res.re('class="article-dochead"><span>(.*?)</span>')[0]
        summary = res.re('id="abspara0010">(.*?)</p>')[0]
        title = res.re('class="title-text">(.*?)</span>')[0]
        item = ArticleItem()
        item['chapter'] = chapter
        item['summary'] = summary
        item['title'] = title
        item['url'] = response.url
        item['volume'] = self.volume
        item['journal'] = 'cell'
        time.sleep(3)
        yield item

    def article_parse(self, response):
        # xpath或正则提取内容
        res = response.xpath(
            '//*[@class="js-article-list article-list-items"]')
        url = res.re('u-margin-s-bottom" href="(.*?)"')
        for u in url:
            site = 'https://www.' + self.allowed_domains[0] + u
            yield scrapy.Request(
                site, callback=self.abstract_parse)

    def parse(self, response):
        # xpath或正则提取内容
        path = os.path.dirname(response.url)
        data = response.xpath(
            ('//*[@class="anchor js-issue-link"]')
        )
        url = f'{path}' + data[0].xpath('@href').extract()[0][8:]
        self.volume = data[0].re('span class="anchor-text">(.*?)</span>')[0]

        # 递归
        yield scrapy.Request(url, callback=self.article_parse)
