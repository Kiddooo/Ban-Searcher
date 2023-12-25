import re
from urllib.parse import urljoin

import dateparser
import scrapy

from banlist_project.items import BanItem
from utils import logger, translate


class BanManagerBonemealSpider(scrapy.Spider):
    name = "BanManagerBonemealSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the BanManagerBonemealSpider object.

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
        Generates the initial requests to scrape data from a website.

        Constructs the URL based on the player's UUID and sends a request to that URL using Scrapy.
        The response is then passed to the `parse` method for further processing.

        Returns:
            None

        Example Usage:
            spider = BanManagerBonemealSpider(username='john', player_uuid='123456', player_uuid_dash='123-456')
            spider.start_requests()
        """
        base_url = "https://mineyourmind.net/bans/index.php/players/"
        url = urljoin(base_url, self.player_uuid)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the HTML response and extract ban records information.

        Args:
            response (scrapy.http.Response): The HTML response received from a website.

        Yields:
            BanItem: A BanItem object with the extracted ban records information.

        """
        # Find all timeline items at once using a CSS selector
        all_timeline_items = response.css("li.timeline, li.timeline-inverted")

        # Iterate over all timeline items
        for item in all_timeline_items:
            # Extract ban reason
            ban_text = item.css("div.timeline-body::text").get().strip()
            ban_reason = ban_text.split(":")[1].strip()

            # Parse the ban date and calculate the timestamp
            ban_date_str = item.css("small.text-muted::attr(title)").get()
            ban_date = self.parse_date(ban_date_str)
            ban_date_timestamp = self.calculate_timestamp(ban_date)

            # Extract ban start date
            ban_start_date_str = item.css("small.text-muted::attr(title)").get()
            ban_start_date = self.parse_date(ban_start_date_str)

            # Check if the ban is permanent using regular expression
            if re.search(r"\bpermanent\b", ban_text):
                ban_end_timestamp = "Permanent"
            else:
                # Get ban length
                ban_length_str = re.search(r"Lasted for (\d+ \w+).", ban_text)
                if ban_length_str:
                    ban_length_str = ban_length_str.group(1)
                    ban_length = dateparser.parse(
                        "in " + ban_length_str
                    ) - dateparser.parse("now")

                    # Calculate ban end date
                    ban_end_date = ban_start_date + ban_length

                    # Convert the ban end date to a Unix timestamp
                    ban_end_timestamp = self.calculate_timestamp(ban_end_date)
                else:
                    ban_end_timestamp = "N/A"

            # Yield a BanItem
            yield BanItem(
                {
                    "source": "bonemeal",
                    "url": response.url,
                    "reason": translate(ban_reason, to_lang="en"),
                    "date": ban_date_timestamp,
                    "expires": ban_end_timestamp,
                }
            )

    def parse_date(self, date_str):
        """
        Parses a date string using the dateparser library.

        Args:
            date_str (str): The date string to be parsed.

        Returns:
            datetime object: The parsed date string converted to a datetime object. If parsing fails, returns None.
        """
        try:
            return dateparser.parse(date_str)
        except Exception as e:
            logger.error(f"Error parsing date: {date_str}: {str(e)}")
            return None

    def calculate_timestamp(self, date):
        """
        Calculate the Unix timestamp from a given date.

        Args:
            date (datetime): The date to calculate the timestamp for.

        Returns:
            int: The Unix timestamp of the given date.
        """
        return int(date.timestamp()) if date else "N/A"
