import scrapy
import tldextract

from banlist_project.items import BanItem
from utils import get_language, translate

# Constants
URL_TEMPLATE = "https://minecraftonline.com/cgi-bin/getplayerinfo?"


class MCOnlineSpider(scrapy.Spider):
    name = "MCOnlineSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the MCOnlineSpider object.

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
        Generates a Scrapy Request object to scrape player information from a website.

        Returns:
            Request: A Scrapy Request object with the URL and callback function.
        """
        url = URL_TEMPLATE + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response received from a website and extract relevant information to create a BanItem object.

        Args:
            response (scrapy.http.Response): The response object received from a website.

        Yields:
            BanItem: A BanItem object containing the parsed ban information.
        """
        # Split the response text by line and semicolon
        ban_info = response.text.split("\n")[3:-1][0].split(";")

        # Extract the relevant information
        source = tldextract.extract(response.url).domain
        url = response.url
        date = int(ban_info[1])
        reason = (
            translate(ban_info[2]) if get_language(ban_info[2]) != "en" else ban_info[2]
        )
        expires = "N/A"

        # Yield a new BanItem with the parsed information
        yield BanItem(
            {
                "source": source,
                "url": url,
                "date": date,
                "reason": reason,
                "expires": expires,
            }
        )
