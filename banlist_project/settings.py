BOT_NAME = "banlist_project"

SPIDER_MODULES = ["banlist_project.spiders"]
NEWSPIDER_MODULE = "banlist_project.spiders"

LOG_LEVEL = "WARNING"

RETRY_TIMES = 1

DOWNLOAD_TIMEOUT = 30

USER_AGENT = "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32
REACTOR_THREADPOOL_MAXSIZE = 128

DOWNLOADER_MIDDLEWARES = {
    "banlist_project.middlewares.FlareSolverrMiddleware": 500,
}

ITEM_PIPELINES = {
    "banlist_project.pipelines.BanPipeline": 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_MAX_DELAY = 60

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
