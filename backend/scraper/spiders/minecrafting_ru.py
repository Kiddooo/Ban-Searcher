import scrapy
import tldextract
from colorama import Fore, Style

from backend.utils import (
    calculate_timestamp,
    get_language,
    logger,
    parse_date,
    translate,
)
from scraper.items import BanItem


class MinecraftingRuSpider(scrapy.Spider):
    name = "MinecraftingRuSpider"

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
        url = f"https://minecrafting.ru/page/bans?user={self.player_username}"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        ban_items = response.css(".ban_item")
        if ban_items:
            for ban_item in ban_items:
                ban_reason = ban_item.css(".ban_reason .ban_reason_value::text").get()
                ban_date = ban_item.css(".ban_date .ban_date_value::attr(title)").get()
                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": (
                            translate(ban_reason)
                            if get_language(ban_reason) != "en"
                            else ban_reason
                        ),
                        "date": calculate_timestamp(parse_date(ban_date, settings={})),
                        "expires": "N/A",
                    }
                )
