import re

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


class DarksCornerSpider(scrapy.Spider):
    name = "DarksCornerSpider"

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
        url = f"https://www.darkscorner.net/bans/user/{self.player_username}"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        table = response.xpath(
            "/html/body/div[3]/div[3]/div/div/div/div[3]/div[1]/div/div/div/table"
        )
        if table:
            for row in table.xpath(".//tr")[1:]:
                columns = row.xpath(".//td")[1:]
                ban_reason = columns[1].xpath("text()").get()
                print(columns[3].xpath("text()").get().lower().strip())
                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": translate(ban_reason)
                        if get_language(ban_reason) != "en"
                        else ban_reason,
                        "date": calculate_timestamp(
                            parse_date(
                                columns[2].xpath("text()").get(),
                                settings={"TIMEZONE": "Etc/UTC"},
                            )
                        ),
                        "expires": "Permanant"
                        if columns[3].xpath("text()").get().strip().lower() == "never"
                        else calculate_timestamp(
                            parse_date(
                                columns[3].xpath("text()").get(),
                                settings={"TIMEZONE": "Etc/UTC"},
                            )
                        ),
                    }
                )
