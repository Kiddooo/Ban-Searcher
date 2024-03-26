
import scrapy
import tldextract
from colorama import Fore, Style

from backend.utils import (
    logger,
)
from scraper.items import BanItem


class DarksCornerSpider(scrapy.Spider):
    name = "MineMenClubSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if not all([username, player_uuid, player_uuid_dash]):
            raise ValueError("Invalid parameters")

        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = f"https://minemen.club/player/{self.player_username}"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        table = response.xpath("/html/body/div/div/main/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/span")
        if table:
                is_banned = table.xpath("text()").get()
                if "currently banned" in is_banned.lower():
                    yield BanItem(
                        {
                            "source": tldextract.extract(response.url).domain,
                            "url": response.url,
                            "reason": "N/A",
                            "date": "N/A",
                            "expires": "N/A"
                        }
                    )
