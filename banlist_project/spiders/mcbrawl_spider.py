import scrapy
import tldextract
from bs4 import BeautifulSoup
from colorama import Fore, Style
from banlist_project.items import BanItem
from utils import calculate_timestamp, get_language, logger, parse_date, translate

# Constants
PLAYER_DOESNT_EXIST = "Player doesn't exist"
NO_BANS = "No bans have been filed."
NO_PERM_BANS = "No permanent bans have been filed."
NO_AUTO_BANS = "No automatic bans have been filed."
BASE_URL = "https://www.mcbrawl.com/history/player/"


class MCBrawlSpider(scrapy.Spider):
    name = "MCBrawlSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the MCBrawlSpider object.

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
        Construct the URL using the base URL and the player's username,
        and yield a scrapy.Request object with the constructed URL and a callback function parse.
        """
        url = BASE_URL + self.player_username
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response and extract ban records.

        Args:
            response (scrapy.http.Response): The response object containing the HTML response from the website.

        Yields:
            BanItem: The ban item object for each ban found in the HTML response.
        """
        soup = BeautifulSoup(response.text, "lxml")

        player_exists_div = soup.find("div", class_="alert alert-danger text-center")
        if player_exists_div and PLAYER_DOESNT_EXIST in player_exists_div.text:
            return

        for ban_type in ["bans", "permbans", "autobans"]:
            ban_elements = soup.find_all("div", class_="tab-pane", id=ban_type)

            if ban_type not in ban_elements[0].text:
                ban_table = ban_elements[0].find(
                    "table", class_="table table-striped table-condensed"
                )

                if ban_table:
                    for row in ban_table.find_all("tr")[1:]:
                        columns = row.find_all("td")
                        ban_reason = columns[0].text

                        yield BanItem(
                            {
                                "source": tldextract.extract(response.url).domain,
                                "url": response.url,
                                "reason": translate(ban_reason)
                                if get_language(ban_reason) != "en"
                                else ban_reason,
                                "date": calculate_timestamp(
                                    parse_date(columns[1].text, settings={}),
                                ),
                                "expires": "N/A"
                                if columns[2].text == ""
                                else calculate_timestamp(parse_date(columns[2].text, settings={})),
                            }
                        )
