from urllib.parse import urljoin

import dateparser
import tldextract
from bs4 import BeautifulSoup
from scrapy import Request, Spider

from banlist_project.items import BanItem
from utils import get_language, translate


class DemocracycraftSpider(Spider):
    name = "DemocracycraftSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the DemocracycraftSpider object.

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
        base_url = "https://www.democracycraft.net/logs/user/"
        url = urljoin(base_url, self.player_username)
        yield Request(url, callback=self.parse, meta={"dont_redirect": True})

    def parse(self, response):
        """
        Parse the HTML response and extract ban records.

        Args:
            response (scrapy.http.Response): The HTML response received from the website.

        Yields:
            BanItem: A BanItem object for each ban record found in the HTML response.
        """
        soup = BeautifulSoup(response.text, "lxml")
        table = self._parse_table(soup)

        if table is not None:
            for row in self._parse_table_rows(table):
                ban_item = self._create_ban_item(response, row)
                yield ban_item

    def _parse_table(self, soup):
        return soup.find("table", class_="results")

    def _parse_table_rows(self, table):
        return table.find_all("tr")[1:]

    def _create_ban_item(self, response, row):
        columns = row.find_all("td")[1:]

        expires_date = columns[3].text.strip()
        ban_date = columns[2].text.strip()
        ban_reason = columns[1].text.strip()

        if expires_date == "Never":
            expires_date = "Permanent"
        else:
            expires_date = int(dateparser.parse(expires_date).timestamp())

        ban_date = int(dateparser.parse(ban_date).timestamp())

        if get_language(ban_reason) != "en":
            ban_reason = translate(ban_reason)

        return BanItem(
            {
                "source": tldextract.extract(response.url).domain,
                "url": response.url,
                "reason": ban_reason,
                "date": ban_date,
                "expires": expires_date,
            }
        )
