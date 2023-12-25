import re
from datetime import timezone

import dateparser
import scrapy
import tldextract
from bs4 import BeautifulSoup

from banlist_project.items import BanItem
from utils import get_language, translate

# Constants for repeated string values
AT = "at"
ST = "st"
ND = "nd"
RD = "rd"
TH = "th"
EN = "en"


class ManaCubeSpider(scrapy.Spider):
    name = "ManaCubeSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the ManaCubeSpider object.

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
        Construct the URL using the player's username and yield a scrapy.Request object with the URL as a callback to the parse method.
        """
        url = f"https://bans.manacube.com/user?user={self.player_username}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Extracts ban records from a website.

        Args:
            response (scrapy.http.Response): The HTTP response object containing the HTML response from the website.

        Yields:
            BanItem: Each BanItem object represents a ban record and contains the source website, URL, ban reason, ban date, and expiry date.
        """
        soup = BeautifulSoup(response.text, "lxml")
        bans_tab = soup.find("div", class_="tab-pane", id="bans")
        table = bans_tab.find("table", class_="table table-striped table-profile")

        if table:
            for row in table.find_all("tr")[1:]:
                columns = row.find_all("td")[1:]
                expires_date_object = self.parse_date(columns[4].text)
                ban_date_object = self.parse_date(columns[3].text)
                ban_reason = columns[0].text
                translated_reason = (
                    translate(ban_reason)
                    if get_language(ban_reason) != "en"
                    else ban_reason
                )

                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": translated_reason,
                        "date": ban_date_object,
                        "expires": expires_date_object,
                    }
                )

    def parse_date(self, date_string: str) -> int:
        """
        Cleans and parses a date string into a timestamp in UTC timezone.

        Args:
            date_string (str): The date string to be parsed.

        Returns:
            int: The parsed date as a timestamp in UTC timezone.
        """
        # Remove "at" from the date string
        date_string = date_string.replace("at", "")

        # Remove ordinal indicators (e.g., "st", "nd", "rd", "th") from the date string
        date_string = re.sub(r"(\d)(st|nd|rd|th)", r"\1", date_string)

        # Remove extra whitespace from the date string
        date_string = " ".join(date_string.split())

        # Parse the cleaned date string into a datetime object
        date_object = dateparser.parse(date_string).replace(tzinfo=timezone.utc)

        # Convert the datetime object to a timestamp in UTC timezone
        timestamp = int(date_object.timestamp())

        return timestamp
