import unicodedata

import dateparser
import scrapy
import tldextract
from colorama import Fore, Style

from scraper.items import BanItem
from backend.utils import get_language, logger, translate

URLS = [
    "http://mc.virtualgate.org/ban/index.php?action=viewplayer&player=",
    # "https://woodymc.de/BanManager/index.php?action=viewplayer&player=", # CLOSED
    "https://bans.piratemc.com/index.php?action=viewplayer&player=",
]


class BanManagerSpider(scrapy.Spider):
    name = "BanManagerSpider"

    def __init__(
        self,
        username=None,
        player_uuid=None,
        player_uuid_dash=None,
        urls=None,
        *args,
        **kwargs,
    ):
        """
        Initialize the BanManagerSpider object.

        Args:
            username (str): The username of the player.
            player_uuid (str): The UUID of the player.
            player_uuid_dash (str): The UUID of the player with dashes.
            urls (list): A list of URLs to scrape ban information from.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        if not all([username, player_uuid, player_uuid_dash]):
            raise ValueError("Invalid parameters")

        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash
        self.urls = URLS

    def start_requests(self):
        """
        Generate initial requests to scrape ban information from multiple URLs.

        Yields:
            scrapy.Request: A request object for each URL with a callback function set to `parse`.
        """
        for url in self.urls:
            logger.info(
                f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
            )
            modified_url = f"{url}{self.player_username}&server=0"
            yield scrapy.Request(url=modified_url, callback=self.parse)

    def parse(self, response):
        """
        Parse the HTML response and extract information about the current ban and previous bans.

        Args:
            response (Response): The response object containing the HTML content.

        Yields:
            BanItem: Representing the current ban and previous bans.
        """

        # Parse current ban
        current_ban_table = response.css("table#current-ban")
        if current_ban_table:
            first_row = current_ban_table.css("tr")[0]
            if first_row.css("td::text").get().strip() != "None":
                current_ban = {}
                for row in current_ban_table.css("tr"):
                    columns = row.css("td")
                    if len(columns) == 2:
                        key = columns[0].css("td::text").get().replace(":", "").lower()
                        value = columns[1].css("td::text").get()
                        if value is None:
                            value = columns[1].css("td.expires span::text").get()
                        current_ban[key] = value

                current_ban = list(current_ban.items())
                ban_start_date_str = current_ban[2][1]
                ban_start_date = dateparser.parse(ban_start_date_str)
                ban_length_str = unicodedata.normalize("NFC", current_ban[0][1])
                permanent_ban_strings = [
                    "Permanent",
                    "Dich sehen wir nicht wieder =:o)",
                ]
                if ban_length_str not in permanent_ban_strings:
                    ban_length = dateparser.parse(
                        "in " + ban_length_str
                    ) - dateparser.parse("now")
                    ban_end_date = ban_start_date + ban_length
                    ban_end_timestamp = int(ban_end_date.timestamp())
                else:
                    ban_end_timestamp = "Permanent"

                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": current_ban[3][1],
                        "date": int(ban_start_date.timestamp()),
                        "expires": ban_end_timestamp,
                    }
                )

        # Parse previous bans
        previous_bans_table = response.css("table#previous-bans")
        if previous_bans_table:
            rows = previous_bans_table.css("tr")
            if len(rows) > 1 and rows[1].css("td::text").get().strip():
                for row in rows[1:]:
                    columns = row.css("td")
                    try:
                        ban_reason = columns[1].css("td::text").get()
                        yield BanItem(
                            {
                                "source": tldextract.extract(response.url).domain,
                                "url": response.url,
                                "reason": translate(ban_reason)
                                if get_language(ban_reason) != "en"
                                else ban_reason,
                                "date": int(
                                    dateparser.parse(
                                        columns[3].css("td::text").get()
                                    ).timestamp()
                                ),
                                "expires": int(
                                    dateparser.parse(
                                        columns[6].css("td::text").get()
                                    ).timestamp()
                                ),
                            }
                        )
                    except IndexError:
                        pass
