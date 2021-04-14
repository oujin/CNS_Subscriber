# 设计流程

1. 在items.py里添加爬虫使用的字段myfield

2. 在spiders文件夹里添加myname_spider.py，解析文本

3. 在pipelines.py里添加自己的MynamePipeline类，验证、处理、保存数据

4. 在settings.py里设置ITEM_PIPELINES，配置自己的Pipeline的优先级(应该是在多个爬虫中的优先级)

5. 启动爬虫

```bash
scrapy crawl myname
```
