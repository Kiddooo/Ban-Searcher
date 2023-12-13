import re
from datetime import timezone

import dateparser
import scrapy
import tldextract
from bs4 import BeautifulSoup

from banlist_project.items import BanItem
from utils import get_language, translate

# Constants for repeated string values
AT = "at"
ST = "st"
ND = "nd"
RD = "rd"
TH = "th"
EN = "en"

# This is a Scrapy Spider for the ManaCube website
class ManaCubeSpider(scrapy.Spider):
    name = "ManaCubeSpider"

    # The constructor takes a username and two forms of the player's UUID
    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(ManaCubeSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    # The start_requests method generates the initial request for the spider
    def start_requests(self):
        # The URL is constructed using the player's username
        url = f"https://manacube.com/members/{self.player_username}.html"
        yield scrapy.Request(url, callback=self.parse)

    # The parse method processes the response from the server
    def parse(self, response):
        # The response is parsed into a BeautifulSoup object for easy manipulation
        soup = BeautifulSoup(response.text, "lxml")

        # The bans tab is located and the ban table is extracted
        bans_tab = soup.find_all("div", class_="tab-pane", id="bans")
        table = bans_tab[0].find("table", class_="table table-striped table-profile")
        if table is not None:
            # Each row in the table (excluding the header) represents a ban
            for row in table.find_all("tr")[1:]:  # Skip the header row
                columns = row.find_all("td")[1:]

                # The expiry and ban dates are parsed into timestamp objects
                expires_date_object = self.parse_date(columns[4].text)
                ban_date_object = self.parse_date(columns[3].text)

                # The ban reason is extracted
                ban_reason = columns[0].text

                # A BanItem is yielded for each ban
                yield BanItem(
                    {
                        "source": tldextract.extract(response.url).domain,
                        "url": response.url,
                        "reason": translate(ban_reason)
                        if get_language(ban_reason) != EN
                        else ban_reason,
                        "date": ban_date_object,
                        "expires": expires_date_object,
                    }
                )

    # Helper function to parse a date string into a timestamp
    def parse_date(self, date_string):
        # The date string is cleaned and parsed into a datetime object
        date_string = date_string.replace(AT, "")
        date_string = re.sub(rf"(\d)({ST}|{ND}|{RD}|{TH})", r"\1", date_string)
        date_string = " ".join(date_string.split())
        date_object = int(
            dateparser.parse(date_string)
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
        return date_object