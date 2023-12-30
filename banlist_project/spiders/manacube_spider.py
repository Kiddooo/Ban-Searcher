import re

import scrapy
import tldextract
from scrapy.selector import Selector

from banlist_project.items import BanItem
from utils import calculate_timestamp, get_language, parse_date, translate

# Constants for repeated string values
AT = "at"
ST = "st"
ND = "nd"
RD = "rd"
TH = "th"
EN = "en"


class ManaCubeSpider(scrapy.Spider):
    name = "ManaCubeSpider"

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
        url = f"https://bans.manacube.com/user?user={self.player_username}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        bans_tab = Selector(response).xpath("//div[@class='tab-pane' and @id='bans']")
        table = bans_tab.xpath("//table[@class='table table-striped table-profile']")

        if table:
            for row in table.xpath(".//tr")[1:]:
                columns = row.xpath(".//td")[1:]
                expires_date_object = self._parse_date(columns[4].xpath("text()").get())
                ban_date_object = self._parse_date(columns[3].xpath("text()").get())
                ban_reason = columns[0].xpath("text()").get()

                if get_language(ban_reason) != "en":
                    translated_reason = translate(ban_reason)
                else:
                    translated_reason = ban_reason

                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": translated_reason,
                        "date": ban_date_object,
                        "expires": expires_date_object,
                    }
                )

    def _parse_date(self, date_string: str) -> int:
        date_string = date_string.replace("at", "")
        date_string = re.sub(r"(\d)(st|nd|rd|th)", r"\1", date_string)
        date_string = " ".join(date_string.split())
        date_object = parse_date(date_string, settings={"TIMEZONE": "UTC"})
        timestamp = calculate_timestamp(date_object)
        return timestamp
