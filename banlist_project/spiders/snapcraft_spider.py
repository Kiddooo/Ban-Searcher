import dateparser
import scrapy
from bs4 import BeautifulSoup
import tldextract
from datetime import datetime
from banlist_project.items import BanItem
from utils import get_language, translate

class SnapcraftSpider(scrapy.Spider):
    name = 'SnapcraftSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(SnapcraftSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        urls = ["https://snapcraft.net/bans/search/" + self.player_username + "/?filter=bans", "https://www.mcfoxcraft.com/bans/search/" + self.player_username + "/?filter=bans"]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('div', class_='ndzn-litebans-table')
        if table is not None:
            rows = table.find_all('div', class_='row')
            for row in rows:
                try:
                    ban_date = int(dateparser.parse(row.find('div', class_='td _date').text.strip()).timestamp())
                except ValueError:
                    try:
                        ban_date = int(dateparser.parse(row.find('div', class_='td _date').text.strip()).timestamp())
                    except ValueError:
                        continue

                ban_expires = row.find('div', class_='td _expires').text.strip().split(" (")[0]
                if ban_expires == 'Expired':
                    ban_expires = 'N/A'
                elif ban_expires == 'Permanent Ban':
                    ban_expires = 'Permanent'
                else:
                    try:
                        ban_expires = int(dateparser.parse(ban_expires).timestamp())
                    except ValueError:
                        print("Failed to parse ban expiry:", ban_expires)
                        ban_expires = 'N/A'

                ban_reason = row.find('div', class_='td _reason').text.strip()
                yield BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': ban_date,
                    'expires': ban_expires
                })