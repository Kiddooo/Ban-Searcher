import json

import scrapy
import tldextract

from banlist_project.items import BanItem
from utils import get_language, logger, translate

# Define constants for static values
BASE_URL = "https://bans-api.cosmic.games/prisons/player/"


class CosmicGamesSpider(scrapy.Spider):
    name = "CosmicGamesSpider"

    # Initialize spider with username and UUIDs
    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the CosmicGamesSpider object.

        Args:
            username (str): The username of the player.
            player_uuid (str): The UUID of the player.
            player_uuid_dash (str): The UUID of the player with dashes.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        if not username or not player_uuid or not player_uuid_dash:
            raise ValueError("Invalid parameters")

        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    # Start requests by constructing URL with username
    def start_requests(self):
        """
        Generate the initial requests to be sent by the spider.

        Returns:
            scrapy.Request: The generated request with the constructed URL and callback function.
        """
        url = BASE_URL + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Process the response received from a website and yield BanItem objects for each ban offence found.

        Args:
            response (scrapy.Response): The response received from the website.

        Yields:
            BanItem: A BanItem object containing information about the ban offence.
        """
        try:
            json_response = json.loads(response.text)
        except json.JSONDecodeError:
            logger.error("Error decoding JSON")
            return

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
