import json
import re
from urllib.parse import urlparse

import dateparser
import scrapy

from banlist_project.items import BanItem
from utils import get_language, translate

# Constants
BASE_URL = "https://bans.guster.ro/api.php?type=player&player={}&page={}&perpage=25"


class GusterSpider(scrapy.Spider):
    name = "GusterSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the GusterSpider object.

        Args:
            username (str): The username of the player.
            player_uuid (str): The UUID of the player.
            player_uuid_dash (str): The UUID of the player with dashes.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        if not all([username, player_uuid, player_uuid_dash]):
            raise ValueError("Invalid parameters")

        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        """
        Generate the initial request to scrape data from a website.

        Returns:
            A scrapy.Request object to initiate the scraping process.
        """
        url = BASE_URL.format(self.player_username, 1)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response from the website and send requests for each page of the ban list.

        Args:
            response (scrapy.Response): The response object containing the ban list data.

        Returns:
            None

        """
        banlist = json.loads(response.text)
        last_page = banlist["lastpage"]

        if banlist["totalpunish"] == "0":
            return

        for page in range(1, last_page + 1):
            url = BASE_URL.format(self.player_username, page)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        """
        Parse the response and extract ban records.

        Args:
            response (scrapy.Response): The response object containing the ban list data.

        Yields:
            dict: A dictionary representing a ban record.

        """
        bans_on_page = json.loads(response.text)["banlist"]
        ban_items = []

        for ban in bans_on_page:
            if (
                isinstance(ban, dict)
                and ban.get("type") == "Ban"
                and all(key in ban for key in ["reason", "date", "expire"])
            ):
                reason = (
                    translate(ban["reason"])
                    if get_language(ban["reason"]) != "en"
                    else ban["reason"]
                )
                date_match = re.search(r"\d{4}-\d{2}-\d{2}", ban["date"])
                date = (
                    int(dateparser.parse(date_match.group()).timestamp())
                    if date_match
                    else None
                )
                expires_match = re.search(r"\d{4}-\d{2}-\d{2}", ban["expire"])
                expires = (
                    int(dateparser.parse(expires_match.group()).timestamp())
                    if expires_match
                    else None
                )

                ban_items.append(
                    BanItem(
                        {
                            "source": urlparse(response.url).hostname,
                            "reason": reason,
                            "url": response.url,
                            "date": date,
                            "expires": expires,
                        }
                    )
                )

        yield ban_items
