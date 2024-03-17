import datetime
from typing import Union

import dateparser
import scrapy
import tldextract
from colorama import Fore, Style

from backend.utils import get_language, logger, translate
from scraper.items import BanItem


class CubevilleSpider(scrapy.Spider):
    """Spider for Cubeville"""

    name = "CubevilleSpider"

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
        url = f"https://www.cubeville.org/cv-site/banlist.php/{self.player_username}"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Find the first table in the parsed HTML
        table = response.css("table")
        # Select all rows
        rows = table.css("tr")
        # Iterate over each row
        for row in rows:
            # Find all columns in the row
            columns = row.css("td")
            # Check if any column contains the player's username
            if any(self.player_username in column.get() for column in columns):
                # Parse the ban date and ban duration text
                banned_at, ban_duration_text = (
                    dateparser.parse(columns[1].css("::text").get()),
                    columns[3].css("::text").get().strip(),
                )
                # Calculate the ban expiration date
                ban_expires = self.get_ban_expires(ban_duration_text, banned_at)
                # Get the ban reason
                ban_reason = columns[2].css("::text").get().strip()
                # Yield a BanItem for each ban
                yield self.create_ban_item(response, ban_reason, banned_at, ban_expires)

    def get_ban_expires(
        self, ban_duration_text: str, banned_at: datetime
    ) -> Union[str, int]:
        if ban_duration_text == "permanent":
            return "Permanent"
        else:
            expiration_date = dateparser.parse(
                f"in {ban_duration_text}", settings={"RELATIVE_BASE": banned_at}
            )
            return int(expiration_date.timestamp())

    def create_ban_item(self, response, ban_reason, banned_at, ban_expires):
        domain = tldextract.extract(response.url).domain
        reason = (
            translate(ban_reason) if get_language(ban_reason) != "en" else ban_reason
        )
        date = int(banned_at.timestamp())

        return BanItem(
            {
                "source": domain,
                "url": response.url,
                "reason": reason,
                "date": date,
                "expires": ban_expires,
            }
        )
