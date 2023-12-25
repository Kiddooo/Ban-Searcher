import dateparser
import scrapy
import tldextract
from bs4 import BeautifulSoup, Comment

from banlist_project.items import BanItem
from utils import get_language, translate

# Constants for various strings used in the code
DATE_FORMAT = "%b %d, %Y %I:%M:%S %p"
UNKNOWN_USER_TEXT = "Unknown User"
BAN_TABLE_CLASS = "table table-bordered"
PERMANENT_BAN_TEXT = "Permanent"
BAN_RECEIVED_COMMENT = "user.ban_received_table_start"
BAN_URL = "https://bans.johnymuffin.com/user/"


class JohnyMuffinSpider(scrapy.Spider):
    # Name of the spider
    name = "JohnyMuffinSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the JohnyMuffinSpider object.

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
        # Start the spider by sending a request to the ban URL
        url = BAN_URL + self.player_uuid_dash
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")

        # If the user is unknown, return
        if soup.find("strong", text=UNKNOWN_USER_TEXT):
            return

        # If the user has received a ban, find the ban table
        if soup.find(
            text=lambda text: isinstance(text, Comment) and BAN_RECEIVED_COMMENT in text
        ):
            ban_table = soup.find_all("table", class_=BAN_TABLE_CLASS)[0]
            if ban_table is not None:
                # For each row in the ban table (skipping the header), create a BanItem
                for row in ban_table.find_all("tr")[1:]:  # Skip the header row
                    columns = row.find_all("td")
                    ban_reason = columns[2].text
                    yield BanItem(
                        {
                            "source": tldextract.extract(response.url).domain,
                            "url": response.url,
                            "reason": translate(ban_reason)
                            if get_language(ban_reason) != "en"
                            else ban_reason,
                            "date": "N/A",
                            "expires": PERMANENT_BAN_TEXT
                            if PERMANENT_BAN_TEXT in columns[3].text
                            else int(dateparser.parse(columns[3].text).timestamp()),
                        }
                    )
