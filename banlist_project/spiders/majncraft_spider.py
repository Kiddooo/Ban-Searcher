from typing import Iterator

import dateparser
import scrapy
import tldextract
from colorama import Fore, Style
from banlist_project.items import BanItem
from utils import get_language, logger, translate

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
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response text from a website and extract ban details from the ban list section.

        :param response: The response object from the website.
        :type response: scrapy.Response
        :return: None
        """
        # Find the section with the list of bans
        ban_list_section = response.css("section.list.list-ban")
        # If the ban list section is found
        if ban_list_section:
            # Find all panels in the ban list section
            panels = ban_list_section.css("div.panel")

            # For each panel, extract the ban details using the `extract_ban_details` method
            for panel in panels:
                ban_item = self.extract_ban_details(panel, response)
                yield from ban_item

    def extract_ban_details(self, panel, response):
        # Extract the ban reason
        ban_reason = panel.xpath(".//div[contains(@class, 'col-sm-7')]/text()[last()]").get().strip()

        # Extract the ban date
        ban_date = panel.xpath(".//div[contains(@class, 'col-sm-1') and contains(@class, 'text-center')][1]/text()").getall()
        ban_date = ' '.join([x.strip() for x in ban_date if x.strip()])

        # Extract the ban expiration
        expires = panel.xpath(".//div[contains(@class, 'col-sm-1') and contains(@class, 'text-center')][2]/text()[last()]").get().strip()

        # Return a BanItem with the extracted details
        yield BanItem(
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