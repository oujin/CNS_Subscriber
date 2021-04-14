import scrapy
from Spider.items import ArticleItem
import time
import re


class ScienceSpider(scrapy.Spider):
    name = "science"
    allowed_domains = ['science.sciencemag.org']
    start_urls = [
        'https://science.sciencemag.org/'
    ]

    def abstract_parse(self, response):
        res = response.xpath('//*[@id="page-top"]')
        title = response.xpath(
            '//*/div[@class="highwire-cite-title"]'
        ).re('title">(.*?)</div>')
        if not title:
            title = response.xpath(
                '//*/div[@class="highwire-cite-title '
                'title-with-subtitle"]'
            ).re('subtitle">(.*?)</div>')
        title = title[0] if title else ''
        chapter = response.xpath('//*[@class="overline"]').extract()[0]
        chapter = re.sub('<.*?>', '|', chapter)
        summary = res.re('<h2>Abstract</h2><p.*?>(.*?)</p>')
        if not summary:
            summary = res.re('<h2>Summary</h2><p.*?>(.*?)</p>')
        summary = summary[0] if summary else ''
        item = ArticleItem()
        item['chapter'] = chapter.strip('|').strip()
        item['summary'] = summary.strip()
        item['title'] = title.strip()
        item['url'] = response.url
        item['volume'] = self.volume.strip()
        item['journal'] = 'science'
        time.sleep(3)
        yield item

    def parse(self, response):
        # xpath或正则提取内容
        self.volume = response.xpath(
            '//*[@class="beta section-title__tagline"]'
        ).re('(.*?)</div>')[0]
        res = response.xpath(
            '//*[@class="highwire-cite-title-wrapper media__headline"]')
        url = res.re('<a href="(.*?)"')[1:-1]
        for u in url:
            site = 'https://' + self.allowed_domains[0] + u
            yield scrapy.Request(
                site, callback=self.abstract_parse)
