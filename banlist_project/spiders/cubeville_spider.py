import scrapy
from banlist_project.items import BanItem
import datetime
import tldextract
from bs4 import BeautifulSoup
from utils import get_language, translate

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class CubevilleSpider(scrapy.Spider):
    name = 'CubevilleSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(CubevilleSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://www.cubeville.org/cv-site/banlist.php/" + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")

        table = soup.find_all("table")
        for row in table[0].find_all("tr")[1:]:
            columns = row.find_all("td")
            if columns[0].text == self.player_username:
                time_units = {
                    "hours": "hours",
                    "days": "days",
                    "minutes": "minutes",
                    "permanent": "permanent",
                }

                for unit in time_units:
                    if unit in columns[3].text:
                        if unit == "permanent":
                            ban_expires = "Permanent"
                        else:
                            expire_amount = int(columns[3].text.replace(unit, "").strip())
                            ban_expires = datetime.datetime.strptime(columns[1].text, DATE_FORMAT) + datetime.timedelta(**{time_units[unit]: expire_amount})
                ban_reason = columns[2].text
                yield BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': int(datetime.datetime.strptime(columns[1].text, DATE_FORMAT).timestamp()
                    ),
                    'expires': ban_expires if isinstance(ban_expires, str) else int(ban_expires.timestamp()),
                })