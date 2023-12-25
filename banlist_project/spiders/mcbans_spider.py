from urllib.parse import urljoin

import dateparser
import scrapy
import tldextract
from bs4 import BeautifulSoup

from banlist_project.items import BanItem
from utils import get_language, translate

# Constants for class names and other strings
TABLE_CLASS = "i-table fullwidth"
PAGINATION_CLASS = "fa fa-step-forward"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class MCBansSpider(scrapy.Spider):
    name = "MCBansSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the MCBansSpider object.

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
        Generate the initial request to scrape data from the MCBans website for a specific player.

        Returns:
            A generator that yields a single `scrapy.Request` object.
        """
        url = f"https://www.mcbans.com/player/{self.player_uuid}/"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response and extract ban data from the MCBans website.

        Args:
            response (scrapy.http.Response): The response object from the initial request.

        Yields:
            BanItem: An item containing information about a ban for a specific player.
        """
        soup = BeautifulSoup(response.text, "lxml")

        while True:
            data = self.extract_data(soup)
            for row in data:
                yield self.create_item(row, response)

            pagination_link = soup.find("span", class_=PAGINATION_CLASS)
            if "disabled" in pagination_link.parent.get("class"):
                break
            else:
                next_page_url = urljoin(response.url, pagination_link.parent["href"])
                yield scrapy.Request(next_page_url, callback=self.parse)

    def extract_data(self, soup):
        """
        Extracts ban data from a table in the HTML using BeautifulSoup.

        Args:
            soup (BeautifulSoup object): The BeautifulSoup object representing the HTML.

        Returns:
            list: A list of dictionaries containing ban data, where each dictionary has the keys 'reason' and 'date'.
        """
        table = soup.find("table", class_=TABLE_CLASS)
        data = []
        if table:
            rows = table.find_all("tr")[1:-1]  # Skip the header row and last row
            for row in rows:
                columns = row.find_all("td")[:-1]
                ban_reason = columns[4].text
                ban_date = columns[5].text
                data.append({"reason": ban_reason, "date": ban_date})
        return data

    def create_item(self, row: dict, response: scrapy.http.Response) -> BanItem:
        """
        Create a BanItem from a row of data.

        Args:
            row (dict): A dictionary containing the ban reason and date.
            response (scrapy.http.Response): The response object from the initial request.

        Returns:
            BanItem: An object representing a ban record, with the source, URL, reason, date, and expires fields.
        """
        reason = row["reason"]
        if get_language(reason) != "en":
            reason = translate(reason)

        date = int(dateparser.parse(row["date"]).timestamp())

        source = tldextract.extract(response.url).domain
        url = response.url

        return BanItem(
            {
                "source": source,
                "url": url,
                "reason": reason,
                "date": date,
                "expires": "N/A",
            }
        )
