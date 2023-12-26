import json
from io import BytesIO

from scrapy import signals
from scrapy.http import HtmlResponse
from twisted.internet import defer, reactor
from twisted.web.client import Agent, FileBodyProducer, readBody
from twisted.web.http_headers import Headers


class BanlistProjectSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        """
        Create a middleware instance and connect the spider_opened signal to the spider_opened method.

        Args:
            cls: The class object.
            crawler: An instance of the Crawler class representing the running crawler.

        Returns:
            An instance of the BanlistProjectSpiderMiddleware class.
        """
        instance = cls()
        # Connect the spider_opened signal to the spider_opened method
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    def spider_opened(self, spider):
        """
        Callback function called when a spider is opened.

        Args:
            self: The instance of the BanlistProjectSpiderMiddleware class.
            spider: The spider object that was opened.

        Returns:
            None

        Example Usage:
            middleware = BanlistProjectSpiderMiddleware()
            spider = Spider()
            middleware.spider_opened(spider)
        """
        spider.logger.info("Spider opened: %s" % spider.name)


class BanlistProjectDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        """
        Create an instance of the BanlistProjectDownloaderMiddleware class and connect the spider_opened signal to the spider_opened method.

        Args:
            cls: The class object.
            crawler: An instance of the Crawler class representing the running crawler.

        Returns:
            An instance of the BanlistProjectDownloaderMiddleware class.
        """
        instance = cls()
        # Connect the spider_opened signal to the spider_opened method
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    def spider_opened(self, spider):
        """
        Callback function called when a spider is opened.

        Args:
            self: The instance of the BanlistProjectDownloaderMiddleware class.
            spider: The spider object that was opened.

        Returns:
            None

        Example Usage:
            middleware = BanlistProjectDownloaderMiddleware()
            spider = Spider()
            middleware.spider_opened(spider)

        This code creates an instance of the BanlistProjectDownloaderMiddleware class and a Spider object.
        It then calls the spider_opened method of the middleware instance, passing the spider object as an argument.
        The method logs a message indicating that the spider has been opened.
        """
        spider.logger.info("Spider opened: %s" % spider.name)


class FlareSolverrMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        """
        Create an instance of the FlareSolverrMiddleware class.

        Args:
            crawler (scrapy.crawler.Crawler): An instance of the Crawler class representing the running crawler.

        Returns:
            FlareSolverrMiddleware: An instance of the FlareSolverrMiddleware class.

        """
        instance = cls()
        # Connect the spider_opened signal to the spider_opened method
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    @defer.inlineCallbacks
    def process_request(self, request, spider):
        """
        Process the request using FlareSolverr.

        :param request: The original request object that needs to be processed by FlareSolverr.
        :type request: scrapy.http.Request
        :param spider: The spider object that is making the request.
        :type spider: scrapy.Spider
        :return: If the request needs to be processed by FlareSolverr and a solution is found with a status code of 200,
                 return an HtmlResponse object. Otherwise, do nothing.
        :rtype: Optional[scrapy.http.HtmlResponse]
        """
        if request.meta.get("flare_solver", False):
            agent = Agent(reactor)
            body = json.dumps(
                {"cmd": "request.get", "url": request.url, "maxTimeout": 60000}
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
        """
        Callback function called when a spider is opened.

        Args:
            self (FlareSolverrMiddleware): The instance of the FlareSolverrMiddleware class.
            spider (Spider): The spider object that was opened.

        Returns:
            None

        Example Usage:
            middleware = FlareSolverrMiddleware()
            spider = Spider()
            middleware.spider_opened(spider)
        """
        spider.logger.info("Spider opened: %s" % spider.name)
