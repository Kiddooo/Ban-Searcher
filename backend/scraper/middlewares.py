import json
from io import BytesIO

from scrapy import signals
from scrapy.http import HtmlResponse
from twisted.internet import defer, reactor
from twisted.web.client import Agent, FileBodyProducer, readBody
from twisted.web.http_headers import Headers


class ScraperSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        instance = cls()
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScraperDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        instance = cls()
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class FlareSolverrMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        instance = cls()
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    @defer.inlineCallbacks
    def process_request(self, request, spider):
        if request.meta.get("flare_solver", False):
            agent = Agent(reactor)
            body = json.dumps(
                {"cmd": "request.get", "url": request.url, "maxTimeout": 30000}
            ).encode("utf8")
            response = yield agent.request(
                b"POST",
                b"http://localhost:8191/v1",
                Headers({"Content-Type": ["application/json"]}),
                FileBodyProducer(BytesIO(body)),
            )
            body = yield readBody(response)
            solution = json.loads(body).get("solution")
            if solution and solution.get("status") == 200:
                return HtmlResponse(
                    url=solution.get("url"),
                    body=solution.get("response"),
                    encoding="utf-8",
                    request=request,
                )

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
