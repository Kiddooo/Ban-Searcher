import dateparser
import scrapy
from bs4 import BeautifulSoup
import tldextract
from datetime import datetime
from banlist_project.items import BanItem
from utils import get_language, translate

class SyuuSpider(scrapy.Spider):
    name = 'SyuuSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(SyuuSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://www.syuu.net/user/" + self.player_uuid_dash
        yield scrapy.Request(url, callback=self.parse, meta={'flare_solver': True})

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table', id='punishment-table', class_='table table-bordered')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                if row.get('class'):
                    pass
                else:
                    if row.find('div').text.lower() == 'ban':
                        columns = row.find_all('td')[1:]
                        ban_url = response.urljoin(columns[0].find('a')['href'])
                        yield scrapy.Request(ban_url, callback=self.parse_ban, meta={'flare_solver': True})

    def parse_ban(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table', class_='table table-striped')
        if table is not None:
            row = table.find_all('tr')[1:]
            ban_reason = row[0].find_all('td')[1].text
            yield BanItem({
                'source': tldextract.extract(response.url).domain,
                'url': response.url,
                'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                'date': int(dateparser.parse(row[2].find_all('td')[1].text).timestamp()),
                'expires': int(dateparser.parse(row[3].find_all('td')[1].text).timestamp())
            })