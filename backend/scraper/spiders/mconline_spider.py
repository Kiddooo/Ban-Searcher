import scrapy
import tldextract
from colorama import Fore, Style

from backend.utils import get_language, logger, translate
from scraper.items import BanItem

# Constants
URL_TEMPLATE = "https://minecraftonline.com/cgi-bin/getplayerinfo?"


class MCOnlineSpider(scrapy.Spider):
    name = "MCOnlineSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if not all([username, player_uuid, player_uuid_dash]):
            raise ValueError("Invalid parameters")

        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = URL_TEMPLATE + self.player_username
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
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
