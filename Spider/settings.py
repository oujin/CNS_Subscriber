BOT_NAME = 'CNS Reader'

SPIDER_MODULES = ['Spider.spiders']
NEWSPIDER_MODULE = 'Spider.spiders'

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/83.0.4103.116 Safari/537.36'
)

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# DOWNLOAD_TIMEOUT = 300

# CONCURRENT_REQUESTS_PER_DOMAIN = 3

ITEM_PIPELINES = {
    'Spider.pipelines.SpiderPipeline': 300,
}

# DOWNLOADER_MIDDLEWARES = {
#    'Spider.middlewares.SpiderDownloaderMiddleware': 543,
# }
