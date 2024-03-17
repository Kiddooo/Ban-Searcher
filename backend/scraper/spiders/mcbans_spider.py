from urllib.parse import urljoin

import dateparser
import scrapy
import tldextract
from bs4 import BeautifulSoup
from colorama import Fore, Style

from backend.utils import get_language, logger, translate
from scraper.items import BanItem

# Constants for class names and other strings
TABLE_CLASS = "i-table fullwidth"
PAGINATION_CLASS = "fa fa-step-forward"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class MCBansSpider(scrapy.Spider):
    name = "MCBansSpider"

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
        url = f"https://www.mcbans.com/player/{self.player_uuid}/"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")

        while True:
            data = self.extract_data(soup)
            for row in data:
                yield self.create_item(row, response)

            pagination_link = soup.find("span", class_=PAGINATION_CLASS)
            if "disabled" in pagination_link.parent.get("class"):
                break
            else:
                next_page_url = urljoin(response.url, pagination_link.parent["href"])
                yield scrapy.Request(next_page_url, callback=self.parse)

    def extract_data(self, soup):
        table = soup.find_all("table", class_=TABLE_CLASS)
        if table:
            data = []
            table = table[1]
            rows = table.find_all("tr")[1:-1]  # Skip the header row and last row
            for row in rows:
                columns = row.find_all("td")[:-1]
                ban_reason = columns[4].text
                ban_date = columns[5].text
                data.append({"reason": ban_reason, "date": ban_date})
        return data

    def create_item(self, row: dict, response: scrapy.http.Response) -> BanItem:
        reason = row["reason"]
        if get_language(reason) != "en":
            reason = translate(reason)

        date = int(dateparser.parse(row["date"]).timestamp())

        source = tldextract.extract(response.url).domain
        url = response.url

        return BanItem(
            {
                "source": source,
                "url": url,
                "reason": reason,
                "date": date,
                "expires": "N/A",
            }
        )
