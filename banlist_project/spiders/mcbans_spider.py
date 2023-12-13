import dateparser
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
import datetime
from banlist_project.items import BanItem
from utils import get_language, translate

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class MCBansSpider(scrapy.Spider):
    name = 'MCBansSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MCBansSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://www.mcbans.com/player/" + self.player_uuid
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        while True:
            table = soup.find_all('table', class_='i-table fullwidth')[1]
            if table is not None:
                for row in table.find_all('tr')[1:-1]: # Skip the header row
                    columns = row.find_all('td')[:-1]
                    ban_reason = columns[4].text
                    yield BanItem({
                        'source': tldextract.extract(response.url).domain,
                        'url': response.url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': int(dateparser.parse(columns[5].text).timestamp()),
                        'expires': 'N/A'
                    })

            pagination_link = soup.find('span', class_='fa fa-step-forward')
            if 'disabled' in pagination_link.parent.get('class'):
                # No more pages
                break
            else:
                next_page_url = urljoin(response.url, pagination_link.parent['href'])
                yield scrapy.Request(next_page_url, callback=self.parse)