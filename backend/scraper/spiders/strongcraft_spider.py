import scrapy
import tldextract
from bs4 import BeautifulSoup
from colorama import Fore, Style

from backend.utils import (
    calculate_timestamp,
    get_language,
    logger,
    parse_date,
    translate,
)
from scraper.items import BanItem

BAN_STATUS_LENGTH_NOT_BANNED = 2
BAN_STATUS_LENGTH_BANNED = 3


class StrongcraftSpider(scrapy.Spider):
    name = "StrongcraftSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the StrongcraftSpider object.

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
        Generate initial requests to scrape player profiles on the Strongcraft website.

        Returns:
            A generator of scrapy.Request objects for each player profile URL.
        """
        url = f"https://www.strongcraft.org/players/{self.player_uuid}/"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse, meta={"dont_redirect": True})

    def parse(self, response):
        """
        Parses the response from a website and extracts ban details if the player is banned.

        Args:
            response (scrapy.Response): The response object containing the HTML content of the website.

        Returns:
            None: If the player profile is not found or the player is not banned.
            BanItem: If the player is banned, the method yields a BanItem object containing the ban details.
        """
        soup = BeautifulSoup(response.text, "lxml")
        if soup.find(
            text="Here you can look for the profile of any player on our network."
        ):
            return

        ban_status_elements = soup.find("div", class_="user-data").find_all("div")
        if len(ban_status_elements) == BAN_STATUS_LENGTH_NOT_BANNED:
            return
        elif len(ban_status_elements) == BAN_STATUS_LENGTH_BANNED:
            if "banned" in ban_status_elements[2].text.lower().strip():
                yield from self.parse_ban_details(soup, response)

    def parse_ban_details(self, soup, response):
        """
        Parses the ban details from the soup object and yields a BanItem.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object representing the HTML content of a website.
            response (scrapy.Response): A scrapy.Response object containing the response from the website.

        Yields:
            BanItem: A BanItem object containing the ban details.
        """
        table = soup.find("div", class_="container youplay-content")
        if table is not None:
            row = table.find_all("p")[2:-1][0]  # Skip the header row
            ban_date, ban_reason = (
                row.text.split("(")[0].replace("The player is banned since ", ""),
                row.text.split("(")[1].split(")")[0],
            )

            yield BanItem(
                {
                    "source": tldextract.extract(response.url).domain,
                    "url": response.url,
                    "reason": translate(ban_reason)
                    if get_language(ban_reason) != "en"
                    else ban_reason,
                    "date": calculate_timestamp(parse_date(ban_date, settings={})),
                    "expires": "Permanent"
                    if row.text.split(",")[1].strip() == "ban is permanent."
                    else row.text.split(",")[1].strip(),
                }
            )
