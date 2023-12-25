# Import necessary libraries
import unicodedata

import dateparser
import scrapy
import tldextract
from bs4 import BeautifulSoup

from banlist_project.items import BanItem
from utils import get_language, translate

# Define constants
URLS = [
    "http://mc.virtualgate.org/ban/index.php?action=viewplayer&player=",
    "https://woodymc.de/BanManager/index.php?action=viewplayer&player=",
    "https://bans.piratemc.com/index.php?action=viewplayer&player=",
]


# Define BanManagerSpider class
class BanManagerSpider(scrapy.Spider):
    name = "BanManagerSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the BanManagerSpider object.

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
        Generate initial requests to scrape ban information from multiple URLs.

        Yields:
            scrapy.Request: A request object for each URL with a callback function set to `parse`.
        """
        for url in URLS:
            modified_url = f"{url}{self.player_username}&server=0"
            yield scrapy.Request(url=modified_url, callback=self.parse)

    def parse(self, response):
        """
        Parse the HTML response and extract information about the current ban and previous bans.

        Args:
            response (Response): The response object containing the HTML content.

        Yields:
            BanItem: Representing the current ban and previous bans.
        """
        soup = BeautifulSoup(response.text, "lxml")

        # Parse current ban
        current_ban = self.parse_current_ban(soup, response)
        if current_ban:
            yield current_ban

        # Parse previous bans
        previous_bans = self.parse_previous_bans(soup, response)
        yield from previous_bans

    def parse_current_ban(self, soup, response):
        """
        Extracts information about the current ban from a HTML table and returns a BanItem object.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML response.
            response (Response): The response object containing the HTML content.

        Returns:
            BanItem: A BanItem object representing the current ban.
        """
        current_ban_table = soup.find("table", id="current-ban")
        if current_ban_table is not None:
            first_row = current_ban_table.find("tr")
            if first_row.find("td").text != "None":
                current_ban = {}
                for row in current_ban_table.find_all("tr"):
                    columns = row.find_all("td")
                    if len(columns) == 2:
                        key = columns[0].text.replace(":", "").lower()
                        value = columns[1].text
                        current_ban[key] = value

                current_ban = list(current_ban.items())
                ban_start_date_str = current_ban[2][1]
                ban_start_date = dateparser.parse(ban_start_date_str)

                ban_length_str = unicodedata.normalize("NFC", current_ban[0][1])
                if (
                    ban_length_str != "Permanent"
                    and ban_length_str.strip() != "Dich sehen wir nicht wieder =:o)"
                ):
                    ban_length = dateparser.parse(
                        "in " + ban_length_str
                    ) - dateparser.parse("now")
                    ban_end_date = ban_start_date + ban_length
                    ban_end_timestamp = int(ban_end_date.timestamp())
                else:
                    ban_end_timestamp = "Permanent"

                return BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": current_ban[3][1],
                        "date": int(ban_start_date.timestamp()),
                        "expires": ban_end_timestamp,
                    }
                )

    def parse_previous_bans(self, soup, response):
        """
        Extracts information about previous bans from a HTML table and returns a list of BanItem objects.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML response.
            response (Response): The response object containing the HTML content.

        Yields:
            BanItem: A BanItem object representing a previous ban.
        """
        previous_bans_table = soup.find("table", id="previous-bans")
        if previous_bans_table:
            rows = previous_bans_table.find_all("tr")
            if len(rows) > 1 and rows[1].find("td").text != "None":
                for row in rows[1:]:
                    columns = row.find_all("td")
                    if len(columns) >= 7:
                        ban_reason = columns[1].text
                        yield BanItem(
                            {
                                "source": tldextract.extract(response.url).domain,
                                "url": response.url,
                                "reason": translate(ban_reason)
                                if get_language(ban_reason) != "en"
                                else ban_reason,
                                "date": int(
                                    dateparser.parse(columns[3].text).timestamp()
                                ),
                                "expires": int(
                                    dateparser.parse(columns[6].text).timestamp()
                                ),
                            }
                        )
