import scrapy
import tldextract
from banlist_project.items import BanItem
from utils import get_language, translate

class MCOnlineSpider(scrapy.Spider):
    name = 'MCOnlineSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MCOnlineSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://minecraftonline.com/cgi-bin/getplayerinfo?" + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        try:
            _ban = response.text.split("\n")[3:-1][0].split(';')
            yield BanItem({
                'source': tldextract.extract(response.url).domain,
                'url': response.url,
                'date': int(_ban[1]),
                'reason': translate(_ban[2]) if get_language(_ban[2]) != 'en' else _ban[2],
                'expires': 'N/A'
            })
        except IndexError:
            pass