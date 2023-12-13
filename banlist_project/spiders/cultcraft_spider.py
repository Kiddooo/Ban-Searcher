import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
import tldextract
from utils import get_language, translate

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

        table = soup.find('table', id='banlist', class_='table-hover')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')[1:]
                expires_date_object = 'Permanent' if columns[3].text.strip() == 'Permaban' else columns[3].text
                ban_date_object = 'N/A' if columns[2].text.strip() == 'Permanent (für immer)' else columns[2].text
                ban_reason = columns[0].text
                yield BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': ban_date_object,
                    'expires': expires_date_object
                })