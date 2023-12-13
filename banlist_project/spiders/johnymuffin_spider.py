import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup, Comment
import tldextract
import datetime
from utils import get_language, translate

DATE_FORMAT = "%b %d, %Y %I:%M:%S %p"

class JohnyMuffinSpider(scrapy.Spider):
    name = 'JohnyMuffinSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(JohnyMuffinSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://bans.johnymuffin.com/user/" + self.player_uuid_dash
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        if soup.find('strong', text='Unknown User'):
            return

        if soup.find(text=lambda text: isinstance(text, Comment) and 'user.ban_received_table_start' in text):
            table = soup.find_all('table', class_='table table-bordered')[0]
            if table is not None:
                for row in table.find_all('tr')[1:]: # Skip the header row
                    columns = row.find_all('td')
                    ban_reason = columns[2].text
                    yield BanItem({
                        'source': tldextract.extract(response.url).domain,
                        'url': response.url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': "N/A",
                        'expires': "Permanent" if "Permanent" in columns[3].text else int(dateparser.parse(columns[3].text).timestamp())
                    })