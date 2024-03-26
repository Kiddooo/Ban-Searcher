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


class SnapcraftSpider(scrapy.Spider):
    # Define the name of the spider
    name = "SnapcraftSpider"

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
        urls = [
            f"https://snapcraft.net/bans/search/{self.player_username}/?filter=bans",
            f"https://www.mcfoxcraft.com/bans/search/{self.player_username}/?filter=bans",
        ]
        for url in urls:
            logger.info(
                f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
            )
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("div", class_="ndzn-litebans-table")
        if table:
            rows = table.find_all("div", class_="row")
            for row in rows:
                ban_date = self.get_ban_date(row)
                ban_expires = self.get_ban_expiry(row)
                ban_reason = row.find("div", class_="td _reason").text.strip()
                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": (
                            translate(ban_reason)
                            if get_language(ban_reason) != "en"
                            else ban_reason
                        ),
                        "date": ban_date,
                        "expires": ban_expires,
                    }
                )

    def get_ban_date(self, row):
        ban_date = calculate_timestamp(
            parse_date(row.find("div", class_="td _date").text.strip(), settings={})
        )
        return ban_date

    def get_ban_expiry(self, row):
        ban_expires = row.find("div", class_="td _expires").text.strip().split(" (")[0]
        if ban_expires == "Expired":
            return "N/A"
        elif ban_expires == "Permanent Ban":
            return "Permanent"
        else:
            return calculate_timestamp(parse_date(ban_expires, settings={}))
