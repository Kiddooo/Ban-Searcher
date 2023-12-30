import json
from urllib.parse import urljoin

import scrapy
import tldextract

from banlist_project.items import BanItem
from utils import get_language, logger, translate

# Define constants for static values
BASE_URL = "https://bans-api.cosmic.games/prisons/player/"


class CosmicGamesSpider(scrapy.Spider):
    name = "CosmicGamesSpider"

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
        url = urljoin(BASE_URL, self.player_username)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        try:
            json_response = json.loads(response.text)
        except json.JSONDecodeError:
            logger.error("Error decoding JSON")
            raise

        try:
            for offence in json_response:
                if offence.get("type", "").lower() == "ban":
                    ban_reason = offence.get("reason", "")
                    translated_reason = (
                        translate(ban_reason)
                        if get_language(ban_reason) != "en"
                        else ban_reason
                    )
                    ban_date = int(offence.get("time", 0) / 1000)
                    ban_expiration = (
                        "Permanent"
                        if offence.get("expiration", 0) == 0
                        else int(offence.get("expiration", 0) / 1000)
                    )

                    yield BanItem(
                        {
                            "source": tldextract.extract(response.url).domain,
                            "url": response.url,
                            "reason": translated_reason,
                            "date": ban_date,
                            "expires": ban_expiration,
                        }
                    )
        except Exception as e:
            logger.error("Error processing ban offences: " + str(e))
            raise
