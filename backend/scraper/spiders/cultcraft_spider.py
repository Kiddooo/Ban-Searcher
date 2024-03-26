import tldextract
from bs4 import BeautifulSoup
from colorama import Fore, Style
from scrapy import Request, Spider

from backend.utils import get_language, logger, translate
from scraper.items import BanItem


class CultcraftSpider(Spider):
    name = "CultcraftSpider"

    PERMANENT = "Permanent"
    PERMABAN = "Permaban"
    PERMANENT_FOREVER = "Permanent (für immer)"

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
        url = f"https://cultcraft.de/bannliste?player={self.player_username}"
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        yield Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")

        # Find the banlist table
        table = soup.find("table", id="banlist", class_="table-hover")
        if table is not None:
            for row in table.find_all("tr")[1:]:  # Skip the header row
                columns = row.find_all("td")[1:]

                # Create a mapping of column names to indices
                column_mapping = {"reason": 0, "date": 2, "expires": 3}

                # Extract ban details using the column mapping
                ban_expiration_date = (
                    self.PERMANENT
                    if columns[column_mapping["expires"]].text.strip() == self.PERMABAN
                    else columns[column_mapping["expires"]].text
                )
                ban_date = (
                    "N/A"
                    if columns[column_mapping["date"]].text.strip()
                    == self.PERMANENT_FOREVER
                    else columns[column_mapping["date"]].text
                )
                ban_reason = columns[column_mapping["reason"]].text

                # Yield a new BanItem
                yield self.create_ban_item(
                    response.url, ban_reason, ban_date, ban_expiration_date
                )

    def create_ban_item(self, url, reason, date, expires):
        reason = translate(reason) if get_language(reason) != "en" else reason
        return BanItem(
            {
                "source": tldextract.extract(url).domain,
                "url": url,
                "reason": reason,
                "date": date,
                "expires": expires,
            }
        )
