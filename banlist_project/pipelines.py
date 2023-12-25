class BanPipeline:
    bans = []
    """
    A Scrapy pipeline for processing items scraped by spiders.
    Each item is appended to the instance's bans list.
    """

    def __init__(self):
        """
        Initialize the pipeline with empty bans list and player details.
        """
        self.username = None
        self.player_uuid = None
        self.player_uuid_dash = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        Class method to create a pipeline instance from a crawler.
        """
        return cls()

    def open_spider(self, spider):
        """
        Called when the spider is opened.
        Retrieves the player details from the spider.
        """
        self.username = spider.player_username
        self.player_uuid = spider.player_uuid
        self.player_uuid_dash = spider.player_uuid_dash

    def process_item(self, item, spider):
        """
        Process each item scraped by the spider.
        The item is appended to the bans list and then returned.
        """
        self.bans.append(item)
        return item
