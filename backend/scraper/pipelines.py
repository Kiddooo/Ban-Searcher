import logging

from colorama import Fore, Style


class BanPipeline:
    bans = []

    def __init__(self):
        self.logger = logging.getLogger("Ban-Scraper")
        self.username = None
        self.player_uuid = None
        self.player_uuid_dash = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        self.username = spider.player_username
        self.player_uuid = spider.player_uuid
        self.player_uuid_dash = spider.player_uuid_dash
        self.logger.info(f"{Fore.BLUE}Starting spider: {spider.name}{Style.RESET_ALL}")

    def process_item(self, item, spider):
        self.logger.info(
            f"{Fore.MAGENTA}{spider.name} | Found ban from source: {item.get('source')}{Style.RESET_ALL}"
        )
        self.bans.append(item)
        return item

    def get_bans(self):
        return self.bans
