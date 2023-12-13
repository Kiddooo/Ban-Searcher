class BanPipeline:

    bans = []

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        return pipeline

    def __init__(self):
        self.username = None
        self.player_uuid = None
        self.player_uuid_dash = None

    def open_spider(self, spider):
        self.username = spider.player_username
        self.player_uuid = spider.player_uuid
        self.player_uuid_dash = spider.player_uuid_dash

    def process_item(self, item, spider):
        self.__class__.bans.append(item)
        return item