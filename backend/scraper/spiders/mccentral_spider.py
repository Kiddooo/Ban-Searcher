import json

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
BASE_URL = "https://mccentral.org/punishments/resources/api/bans.php?uuid="


class MCCentralSpider(scrapy.Spider):
    name = "MCCentralSpider"

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
        url = f"{BASE_URL}{self.player_uuid}"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        json_response = json.loads(response.text)["results"]

        if json_response["offence_count"] != 0:
            for offence in json_response["offences"]:
                if (
                    offence["severity"] in ["1", "3"]
                    and offence["timeleft"] != "Appealed"
                ):
                    ban_reason = offence["reason"]
                    domain = tldextract.extract(response.url).domain
                    date_str = (
                        offence["datetime"]
                        .replace("st", "")
                        .replace("nd", "")
                        .replace("rd", "")
                        .replace("th", "")
                        .replace("Augu", "August")
                    )
                    date = calculate_timestamp(parse_date(date_str, settings={}))
                    expires = "Permanent" if offence["timeleft"] == "Forever" else "N/A"

                    yield BanItem(
                        {
                            "source": domain,
                            "url": response.url,
                            "reason": (
                                translate(ban_reason)
                                if get_language(ban_reason) != "en"
                                else ban_reason
                            ),
                            "date": date,
                            "expires": expires,
                        }
                    )
