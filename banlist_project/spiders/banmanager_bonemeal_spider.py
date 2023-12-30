import re
from urllib.parse import urljoin

import dateparser
import scrapy

from banlist_project.items import BanItem
from utils import calculate_timestamp, parse_date, translate


class BanManagerBonemealSpider(scrapy.Spider):
    name = "BanManagerBonemealSpider"

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
        base_url = "https://mineyourmind.net/bans/index.php/players/"
        url = urljoin(base_url, self.player_uuid)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        all_timeline_items = response.css("li.timeline, li.timeline-inverted")

        for item in all_timeline_items:
            ban_reason = self.extract_ban_reason(item)
            ban_date = self.parse_ban_date(item)
            ban_date_timestamp = calculate_timestamp(ban_date)
            ban_start_date = self.parse_ban_start_date(item)
            ban_end_timestamp = self.calculate_ban_end_timestamp(item, ban_start_date)

            yield BanItem(
                {
                    "source": "bonemeal",
                    "url": response.url,
                    "reason": translate(ban_reason, to_lang="en"),
                    "date": ban_date_timestamp,
                    "expires": ban_end_timestamp,
                }
            )

    def extract_ban_reason(self, item):
        ban_text = item.css("div.timeline-body::text").get().strip()
        ban_reason = ban_text.split(":")[1].strip()
        return ban_reason

    def parse_ban_date(self, item):
        ban_date_str = item.css("small.text-muted::attr(title)").get()
        return parse_date(ban_date_str)

    def parse_ban_start_date(self, item):
        ban_start_date_str = item.css("small.text-muted::attr(title)").get()
        return parse_date(ban_start_date_str)

    def calculate_ban_end_timestamp(self, item, ban_start_date):
        ban_text = item.css("div.timeline-body::text").get().strip()
        if re.search(r"\bpermanent\b", ban_text):
            return "Permanent"
        else:
            ban_length_str = item.css("div.timeline-body").re_first(
                r"Lasted for (\d+ \w+)."
            )
            if ban_length_str:
                ban_length = dateparser.parse(
                    "in " + ban_length_str
                ) - dateparser.parse("now")
                ban_end_date = ban_start_date + ban_length
                return calculate_timestamp(ban_end_date)
            else:
                return "N/A"
