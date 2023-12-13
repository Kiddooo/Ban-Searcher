import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
from datetime import datetime
import tldextract
from utils import get_language, translate

class DemocracycraftSpider(scrapy.Spider):
    name = 'DemocracycraftSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(DemocracycraftSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://www.democracycraft.net/logs/user/" + self.player_username
        yield scrapy.Request(url, callback=self.parse, meta={'dont_redirect': True})

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        table = soup.find('table', class_='results')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')[1:]
                expires_date_object = 'Permanent' if columns[3].text.strip() == 'Never' else  int(dateparser.parse(columns[3].text).timestamp())
                ban_date_object = int(dateparser.parse(columns[2].text).timestamp())
                ban_reason = columns[1].text
                yield BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': ban_date_object,
                    'expires': expires_date_object
                })