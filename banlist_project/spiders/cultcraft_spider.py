import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
import tldextract
from utils import get_language, translate

# Constants for magic strings
PERMANENT = 'Permanent'
PERMABAN = 'Permaban'
PERMANENT_FOREVER = 'Permanent (für immer)'

class CultcraftSpider(scrapy.Spider):
    name = 'CultcraftSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(CultcraftSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://cultcraft.de/bannliste?player=" + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        # Find the banlist table
        table = soup.find('table', id='banlist', class_='table-hover')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')[1:]

                # Extract ban details
                ban_expiration_date = PERMANENT if columns[3].text.strip() == PERMABAN else columns[3].text
                ban_date = 'N/A' if columns[2].text.strip() == PERMANENT_FOREVER else columns[2].text
                ban_reason = columns[0].text

                # Yield a new BanItem
                yield self.create_ban_item(response.url, ban_reason, ban_date, ban_expiration_date)

    def create_ban_item(self, url, reason, date, expires):
        """Creates a BanItem with translated reason if necessary."""
        reason = translate(reason) if get_language(reason) != 'en' else reason
        return BanItem({
            'source': tldextract.extract(url).domain,
            'url': url,
            'reason': reason,
            'date': date,
            'expires': expires
        })