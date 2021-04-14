import scrapy
from Spider.items import ArticleItem
import time


class NatureSpider(scrapy.Spider):
    name = "nature"
    allowed_domains = ['nature.com']
    start_urls = [
        'https://www.nature.com/nature/volumes/'
    ]

    def article_parse(self, response):
        volume = response.xpath(
            '//*[@class="extra-tight-line-height"]/text()'
        ).extract()[0]
        articles = response.xpath(
            '//*[@itemtype="http://schema.org/ScholarlyArticle"]'
        )
        for a in articles:
            chapter = a.re('data-test="article.type">(.*?)<')[0]
            summary = a.re('<p>(.*?)</p>')
            summary = summary[0] if summary else ''
            title = a.re('(.*?)</a>')[0]
            url = a.re('<a href="(.*?)"')[0]
            url = f'https://www.{self.allowed_domains[0]}{url}'
            item = ArticleItem()
            item['chapter'] = chapter.strip()
            item['summary'] = summary.strip()
            item['title'] = title.strip()
            item['url'] = url.strip()
            item['volume'] = volume.strip()
            item['journal'] = 'nature'
            time.sleep(3)
            yield item

    def journal_parse(self, response):
        # xpath或正则提取内容
        url = response.xpath(
            '//*[@class="kill-hover flex-box-item"]/@href'
        ).extract()[0]
        url = f'https://www.{self.allowed_domains[0]}{url}'
        yield scrapy.Request(
            url, callback=self.article_parse)

    def parse(self, response):
        # xpath或正则提取内容
        url = response.xpath(
            '//*[@data-track-action="view volume"]/@href'
        ).extract()[0]
        url = f'https://www.{self.allowed_domains[0]}{url}'
        # 递归
        yield scrapy.Request(url, callback=self.journal_parse)
