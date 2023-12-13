import dateparser
import scrapy
from bs4 import BeautifulSoup
import tldextract
import datetime
from banlist_project.items import BanItem
from utils import get_language, translate

PLAYER_DOESNT_EXIST = "Player doesn't exist"
NO_BANS = "No bans have been filed."
NO_PERM_BANS = "No permanent bans have been filed."
NO_AUTO_BANS = "No automatic bans have been filed."

class MCBrawlSpider(scrapy.Spider):
    name = 'MCBrawlSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MCBrawlSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://www.mcbrawl.com/history/player/" + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        bans = []
        for ban_type in ['bans', 'permbans', 'autobans']:
            soup = BeautifulSoup(response.text, 'lxml')

            if soup.find('div', class_='alert alert-danger text-center'):
                if PLAYER_DOESNT_EXIST in soup.find('div', class_='alert alert-danger text-center').text:
                    return

            ban_element = soup.find_all('div', class_='tab-pane', id=ban_type)

            if ban_type not in ban_element[0].text:
                table = ban_element[0].find('table', class_='table table-striped table-condensed')
                if table is not None:
                    for row in table.find_all('tr')[1:]: # Skip the header row
                        columns = row.find_all('td')
                        ban_reason = columns[0].text
                        try:
                            ban_reason_lang = get_language(ban_reason)
                        except IndexError:
                            ban_reason_lang = 'en'
                        yield BanItem({
                            'source': tldextract.extract(response.url).domain,
                            'url': response.url,
                            'reason': translate(ban_reason) if ban_reason_lang != 'en' else ban_reason,
                            'date': int(dateparser.parse(columns[1].text).timestamp()),
                            'expires': 'N/A' if columns[2].text == "" else int(dateparser.parse(columns[2].text).timestamp()),
                        })