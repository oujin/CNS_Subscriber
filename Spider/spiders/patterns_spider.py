import scrapy
from Spider.items import ArticleItem


class CellSpider(scrapy.Spider):
    name = "patterns"
    allowed_domains = ['www.cell.com']
    start_urls = [
        'https://www.cell.com/patterns/current'
    ]

    def parse(self, response):
        volume = response.xpath(
            '//*[@class="toc-header__volume"]/text()'
        ).extract()[0]
        issue = response.xpath(
            '//*[@class="toc-header__issue"]/text()'
        ).extract()[0]
        volume = f'{volume}, {issue}'
        sections = response.xpath(
            '//*[@class="toc__section"]'
        )
        for s in sections:
            chapter = s.re('class="toc__heading__header  ".*?>(.*?)<')
            chapter = chapter[0] if chapter else ''
            matchs = s.re('class="toc__item__title"><a href='
                          '"([^\"]*?)">(.*?)</a>.*?<div class='
                          '"toc__item__brief">(.*?)</div>')
            for i in range(0, len(matchs), 3):
                item = ArticleItem()
                item['title'] = matchs[i+1].strip()
                item['chapter'] = chapter.strip()
                item['summary'] = matchs[i+2].strip()
                url = matchs[i].strip()
                item['url'] = f'https://{self.allowed_domains[0]}{url}'
                item['volume'] = volume.strip()
                item['journal'] = 'patterns'
                yield item
