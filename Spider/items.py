import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    chapter = scrapy.Field()
    summary = scrapy.Field()
    volume = scrapy.Field()
    journal = scrapy.Field()
