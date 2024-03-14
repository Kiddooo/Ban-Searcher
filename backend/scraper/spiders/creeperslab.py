import json
from urllib.parse import urljoin

import scrapy
import tldextract
import dateparser
from colorama import Fore, Style

from backend.utils import get_language, logger, translate
from scraper.items import BanItem


class CreepersLabSpider(scrapy.Spider):
    name = "CreepersLabSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if not username or not player_uuid or not player_uuid_dash:
            raise ValueError("Invalid parameters")

        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://www.creeperslab.net/api/v1/minecraft/bans"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        json_response = json.loads(response.text)

        for player_ban_id in json_response:
            json_ban = json_response[player_ban_id]
            if (
                json_ban["uuid"] == self.player_uuid_dash
                and json_ban["mc_type"].lower() == "java"
            ):
                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": "https://www.creeperslab.net/wall_of_shame.php",
                        "reason": (
                            translate(json_ban["reason"])
                            if get_language(json_ban["reason"]) != "en"
                            else json_ban["reason"]
                        ),
                        "date": (
                            "N/A"
                            if not json_ban["begin"]
                            else int(dateparser.parse(json_ban["begin"]).timestamp())
                        ),
                        "expires": (
                            "Permanent"
                            if json_ban["end"] == None
                            else int(dateparser.parse(json_ban["end"]).timestamp())
                        ),
                    }
                )
