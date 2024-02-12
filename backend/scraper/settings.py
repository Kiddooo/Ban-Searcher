BOT_NAME = "scraper"


SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

LOG_ENABLED = False
LOG_LEVEL = "DEBUG"
RETRY_TIMES = 1
DOWNLOAD_TIMEOUT = 30

USER_AGENT = "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32
REACTOR_THREADPOOL_MAXSIZE = 128

DOWNLOADER_MIDDLEWARES = {
    "scraper.middlewares.FlareSolverrMiddleware": 500,
}

ITEM_PIPELINES = {
    "scraper.pipelines.BanPipeline": 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_MAX_DELAY = 60

DNSCACHE_ENABLED = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


DOWNLOADER_STATS = False
STATS_DUMP = False
