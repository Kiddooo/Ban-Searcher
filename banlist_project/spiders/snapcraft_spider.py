import dateparser
import scrapy
import tldextract
from bs4 import BeautifulSoup

from banlist_project.items import BanItem
from utils import get_language, logger, translate


class SnapcraftSpider(scrapy.Spider):
    # Define the name of the spider
    name = "SnapcraftSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the SnapcraftSpider object.

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
        Generate initial requests to scrape data from two different URLs.

        Returns:
            generator: A generator that yields scrapy.Request objects for each URL.
        """
        urls = [
            f"https://snapcraft.net/bans/search/{self.player_username}/?filter=bans",
            f"https://www.mcfoxcraft.com/bans/search/{self.player_username}/?filter=bans",
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response and extract ban data.

        Args:
            response (scrapy.http.Response): The response object containing the HTML response from the website.

        Yields:
            BanItem: A BanItem object with the extracted ban data.
        """
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("div", class_="ndzn-litebans-table")
        if table:
            rows = table.find_all("div", class_="row")
            for row in rows:
                ban_date = self.get_ban_date(row)
                ban_expires = self.get_ban_expiry(row)
                ban_reason = row.find("div", class_="td _reason").text.strip()
                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": translate(ban_reason)
                        if get_language(ban_reason) != "en"
                        else ban_reason,
                        "date": ban_date,
                        "expires": ban_expires,
                    }
                )

    def get_ban_date(self, row):
        """
        Parses the ban date from a given HTML row.

        Args:
            row (BeautifulSoup object): The HTML row containing the ban date information.

        Returns:
            int or str: The ban date as an integer timestamp or 'N/A' if the parsing fails.
        """
        try:
            ban_date = int(
                dateparser.parse(
                    row.find("div", class_="td _date").text.strip()
                ).timestamp()
            )
        except ValueError as e:
            logger.error(f"Failed to parse ban date: {e}")
            ban_date = "N/A"
        return ban_date

    def get_ban_expiry(self, row):
        """
        Parse the ban expiry date from the given HTML row and return it as an integer timestamp or 'N/A' if parsing fails.

        Args:
            row (BeautifulSoup object): The HTML row containing the ban expiry date information.

        Returns:
            int or str: The ban expiry date as an integer timestamp or 'N/A' if parsing fails.
        """
        ban_expires = row.find("div", class_="td _expires").text.strip().split(" (")[0]
        if ban_expires == "Expired":
            return "N/A"
        elif ban_expires == "Permanent Ban":
            return "Permanent"
        else:
            try:
                return int(dateparser.parse(ban_expires).timestamp())
            except ValueError:
                logger.error("Failed to parse ban expiry:", ban_expires)
                return "N/A"
