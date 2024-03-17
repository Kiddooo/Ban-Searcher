import json
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

# Constants
BASE_URL = "https://bans.guster.ro/api.php?type=player&player={}&page={}&perpage=25"


class GusterSpider(scrapy.Spider):
    name = "GusterSpider"

    custom_settings = {
        "DUPEFILTER_CLASS": "scrapy.dupefilters.BaseDupeFilter",
    }

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
        url = BASE_URL.format(self.player_username, 1)
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        banlist = json.loads(response.text)
        last_page = banlist["lastpage"]

        if banlist["totalpunish"] == "0":
            return

        for page in range(1, last_page + 1):
            url = BASE_URL.format(self.player_username, page)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        bans_on_page = json.loads(response.text)["banlist"]

        for ban in bans_on_page:
            if (
                isinstance(ban, dict)
                and ban.get("type") == '<td class="ban">Ban</td>'
                and all(key in ban for key in ["reason", "date", "expire"])
            ):
                reason = (
                    translate(ban["reason"])
                    if get_language(ban["reason"]) != "en"
                    else ban["reason"]
                )
                date = calculate_timestamp(parse_date(ban["date"], settings={}))

                expires_match = re.search(
                    r"\d{2}:\d{2}:\d{2} \d{2}.\d{2}.\d{4}", ban["expire"]
                )
                expires = (
                    calculate_timestamp(parse_date(expires_match.group(), settings={}))
                    if expires_match
                    else "N/A"
                )

                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "reason": reason,
                        "url": response.url,
                        "date": date,
                        "expires": expires,
                    }
                )
