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

# Constants for better readability
HEADER_ROW_INDEX = 1


class SyuuSpider(scrapy.Spider):
    name = "SyuuSpider"

    # Initialize spider with player details
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
        url = f"https://www.syuu.net/user/{self.player_uuid_dash}"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse, meta={"flare_solver": True})

    def parse(self, response):
        parsed_html = BeautifulSoup(response.text, "lxml")
        punishment_table = parsed_html.find(
            "table", id="punishment-table", class_="table table-bordered"
        )
        if punishment_table:
            rows = punishment_table.find_all("tr")[1:]
            for row in rows:
                if row.get("class"):
                    continue
                if row.find("div").text.lower() == "ban":
                    columns = row.find_all("td")[1:]
                    ban_url = response.urljoin(columns[0].find("a")["href"])
                    yield scrapy.Request(
                        ban_url, callback=self.parse_ban, meta={"flare_solver": True}
                    )

    def parse_ban(self, response):
        # Parse the HTML response using BeautifulSoup
        parsed_html = BeautifulSoup(response.text, "lxml")

        # Find the ban details table in the parsed HTML
        ban_details_table = parsed_html.find("table", class_="table table-striped")

        # If the ban details table is found
        if ban_details_table is not None:
            # Get all rows in the table, skipping the header row
            rows = ban_details_table.find_all("tr")[1:]

            # Get the ban reason
            ban_reason = rows[0].find_all("td")[1].text

            # Extract the source URL, translated ban reason, ban date, and expiration date from the respective rows of the table
            source = tldextract.extract(response.url).domain
            url = response.url
            reason = (
                translate(ban_reason)
                if get_language(ban_reason) != "en"
                else ban_reason
            )
            date = calculate_timestamp(
                parse_date(rows[2].find_all("td")[1].text, settings={})
            )
            expires = calculate_timestamp(
                parse_date(rows[3].find_all("td")[1].text, settings={})
            )

            # Create a BanItem object with the extracted information
            ban_item = BanItem(
                {
                    "source": source,
                    "url": url,
                    "reason": reason,
                    "date": date,
                    "expires": expires,
                }
            )

            # Yield the BanItem object
            yield ban_item
