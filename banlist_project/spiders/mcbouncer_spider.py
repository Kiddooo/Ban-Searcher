import scrapy
import scrapy.http
import tldextract
from bs4 import BeautifulSoup
from colorama import Fore, Style

from banlist_project.items import BanItem
from utils import calculate_timestamp, get_language, logger, parse_date, translate

BASE_URL = "https://mcbouncer.com/u/{}/bansFor"


class MCBouncerSpider(scrapy.Spider):
    name = "MCBouncerSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the MCBouncerSpider object.

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
        Generate the initial request to scrape data from a website.

        Returns:
            A generator that yields scrapy.Request objects with the URL and callback function.
        """
        url = BASE_URL.format(self.player_uuid)
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response and extract data from it.

        Args:
            response (scrapy.Response): The response object containing the HTML content of the page to be parsed.

        Yields:
            scrapy.Request: A new request to the next page.
        """
        parsed_html = BeautifulSoup(response.text, "lxml")
        while True:
            yield from self.parse_table(parsed_html, response)

            next_button = parsed_html.find("a", string="»")
            if next_button is not None:
                next_button_parent = next_button.find_parent("li")

                if "disabled" in next_button_parent.get("class", []):
                    break

                next_page_url = response.urljoin(next_button["href"])
                yield scrapy.Request(next_page_url, callback=self.parse)
            else:
                break

    def parse_table(self, parsed_html: BeautifulSoup, response: scrapy.http.Response):
        """
        Extracts data from a table in the HTML response.

        Args:
            parsed_html (BeautifulSoup): The parsed HTML content of the page.
            response (scrapy.Response): The response object containing the HTML content of the page to be parsed.

        Yields:
            BanItem: A BanItem object with the extracted data from each row in the table.
        """
        # Extract the ban reason
        ban_reason = response.css("table.table tbody tr td:nth-child(2) a::text").get()

        # Extract the ban date
        ban_date = response.css("table.table tbody tr td:nth-child(3)::text").get()
        yield BanItem(
            {
                "source": tldextract.extract(response.url).domain,
                "url": response.url,
                "reason": translate(ban_reason)
                if get_language(ban_reason) != "en"
                else ban_reason,
                "date": calculate_timestamp(
                    parse_date(ban_date.replace("\xa0", " "), settings={})
                ),
                "expires": "N/A",
            }
        )
