import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
from datetime import datetime
import tldextract
from utils import translate, get_language

class MajncraftSpider(scrapy.Spider):
    name = 'MajncraftSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MajncraftSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://server.majncraft.cz/player/" + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        table = soup.find('section', class_='list list-ban')
        if table is not None:
            panels = table.find_all('div', class_='panel')
            for panel in panels:
                row = panel.find('div', class_='row')
                cols = row.find_all('div')
                ban_reason = cols[1].contents[3].strip()
                ban_date = cols[2].get_text().strip().split()[1]
                ban_date = ban_date[:-5] + ' ' + ban_date[-5:]
                expires = cols[3].get_text().strip().split()[1]
                print(dateparser.parse('30.11.2023 04:05'))
                yield BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': int(dateparser.parse(ban_date).timestamp()),
                    'expires': "Permanent" if expires == "Nikdy" else int(dateparser.parse(expires).timestamp())
                })