import json
from scrapy import signals
from scrapy.http import HtmlResponse
from twisted.internet import defer
from twisted.web.client import Agent, readBody, FileBodyProducer
from twisted.web.http_headers import Headers
from twisted.internet import reactor
from io import BytesIO

# Middleware for processing the spider
class BanlistProjectSpiderMiddleware:
    """Middleware for processing the spider."""

    # Class method to create an instance of the middleware
    @classmethod
    def from_crawler(cls, crawler):
        """Create an instance of the middleware."""
        instance = cls()
        # Connect the spider_opened signal to the spider_opened method
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    # Method to log when the spider is opened
    def spider_opened(self, spider):
        """Log when the spider is opened."""
        spider.logger.info("Spider opened: %s" % spider.name)


# Middleware for processing the downloader
class BanlistProjectDownloaderMiddleware:
    """Middleware for processing the downloader."""

    # Class method to create an instance of the middleware
    @classmethod
    def from_crawler(cls, crawler):
        """Create an instance of the middleware."""
        instance = cls()
        # Connect the spider_opened signal to the spider_opened method
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    # Method to log when the spider is opened
    def spider_opened(self, spider):
        """Log when the spider is opened."""
        spider.logger.info("Spider opened: %s" % spider.name)


# Middleware for handling Cloudflare's anti-bot page
class FlareSolverrMiddleware:
    """Middleware for handling Cloudflare's anti-bot page."""

    # Class method to create an instance of the middleware
    @classmethod
    def from_crawler(cls, crawler):
        """Create an instance of the middleware."""
        instance = cls()
        # Connect the spider_opened signal to the spider_opened method
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    # Method to process the request using FlareSolverr
    @defer.inlineCallbacks
    def process_request(self, request, spider):
        """Process the request using FlareSolverr."""
        # If the request needs to be processed by FlareSolverr
        if request.meta.get('flare_solver', False):
            agent = Agent(reactor)
            # Prepare the body of the request to FlareSolverr
            body = json.dumps({
                'cmd': 'request.get',
                'url': request.url,
                'maxTimeout': 60000
            }).encode('utf8')
            # Send the request to FlareSolverr
            response = yield agent.request(
                b'POST',
                b'http://localhost:8191/v1',  # FlareSolverr API URL
                Headers({'Content-Type': ['application/json']}),
                FileBodyProducer(BytesIO(body))
            )
            # Read the body of the response
            body = yield readBody(response)
            # Get the solution from the response
            solution = json.loads(body).get('solution')
            # If the solution is found and the status is 200
            if solution and solution.get('status') == 200:
                # Return the solution as an HtmlResponse
                defer.returnValue(HtmlResponse(
                    url=solution.get('url'),
                    body=solution.get('response'),
                    encoding='utf-8',
                    request=request
                ))

    # Method to log when the spider is opened
    def spider_opened(self, spider):
        """Log when the spider is opened."""
        spider.logger.info('Spider opened: %s' % spider.name)