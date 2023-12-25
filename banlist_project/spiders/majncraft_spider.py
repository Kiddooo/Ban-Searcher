# Import necessary libraries
from typing import Iterator

import dateparser
import scrapy
import tldextract
from bs4 import BeautifulSoup

from banlist_project.items import BanItem
from utils import get_language, translate

# Define constants for static values
PERMANENT = "Permanent"
NEVER = "Nikdy"


# Define the spider class
class MajncraftSpider(scrapy.Spider):
    # Set the name of the spider
    name = "MajncraftSpider"

    # Initialize the spider with necessary parameters
    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the MajncraftSpider object.

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

    def start_requests(self) -> Iterator[scrapy.Request]:
        """
        Construct the URL and yield a Scrapy request to that URL with the `parse` method as the callback.
        """
        url = f"https://server.majncraft.cz/player/{self.player_username}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response text from a website and extract ban details from the ban list section.

        :param response: The response object from the website.
        :type response: scrapy.Response
        :return: None
        """
        # Parse the response text with BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")

        # Find the section with the list of bans
        ban_list_section = soup.find("section", class_="list list-ban")

        # If the ban list section is found
        if ban_list_section:
            # Find all panels in the ban list section
            panels = ban_list_section.find_all("div", class_="panel")

            # For each panel, extract the ban details using the `extract_ban_details` method
            for panel in panels:
                ban_item = self.extract_ban_details(panel, response)
                yield ban_item

    def extract_ban_details(self, panel, response):
        """
        Extracts ban details from a panel.

        Args:
            panel (BeautifulSoup object): The panel containing the ban details.
            response (scrapy.Response object): The response object from the website.

        Returns:
            BanItem object: The BanItem object containing the extracted ban details.
        """
        # Find the row in the panel
        row = panel.find("div", class_="row")
        # Find all divs in the row, which contain the ban details
        ban_details = row.find_all("div")

        # Extract the ban reason, date, and expiration from the ban details
        ban_reason = ban_details[1].contents[3].strip()
        ban_date = ban_details[2].get_text().strip().split()[1]
        ban_date = ban_date[:-5] + " " + ban_date[-5:]
        expires = ban_details[3].get_text().strip().split()[1]

        # Return a BanItem with the extracted details
        return BanItem(
            {
                "source": tldextract.extract(response.url).domain,
                "url": response.url,
                "reason": translate(ban_reason)
                if get_language(ban_reason) != "en"
                else ban_reason,
                "date": int(dateparser.parse(ban_date).timestamp()),
                "expires": PERMANENT
                if expires == NEVER
                else int(dateparser.parse(expires).timestamp()),
            }
        )
