import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
from utils import USER_AGENT, get_language, translate
from urllib.parse import urlparse
from datetime import datetime
import json

class GusterSpider(scrapy.Spider):
    name = 'GusterSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(GusterSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://bans.guster.ro/api.php?type=player&player=" + self.player_username + "&page=1&perpage=25"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        banlist = json.loads(response.text)
        last_page = banlist['lastpage']
        if banlist['totalpunish'] == '0':
            return

        base_url: str = response.url.split('?')[0] + "?type=player&player={}&page={}&perpage=25"

        for page in range(1, last_page + 1):
            yield scrapy.Request(base_url.format(self.player_username, page), callback=self.parse_page)

    def parse_page(self, response):
        _bans_list = json.loads(response.text)['banlist']

        for ban in _bans_list:
            if isinstance(ban, dict) and 'Ban' in ban.get('type') and all(key in ban for key in ['reason', 'date', 'expire']):
                yield BanItem({
                    'source': urlparse(response.url).hostname,
                    'reason': translate(ban['reason']) if get_language(ban['reason']) != 'en' else ban['reason'],
                    'url': response.url,
                    'date': int(dateparser.parse(BeautifulSoup(ban['date'], 'lxml').text).timestamp()),
                    'expires': 'Permanant' if 'Never' in ban['expire'] else 'N/A' if 'Expired' in ban['expire'] else int(dateparser.parse(BeautifulSoup(ban['expire'], 'lxml').text).timestamp())
                })