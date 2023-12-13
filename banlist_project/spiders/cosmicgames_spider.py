import scrapy
from banlist_project.items import BanItem
import json
import tldextract
from utils import get_language, translate

class CosmicGamesSpider(scrapy.Spider):
    name = 'CosmicGamesSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(CosmicGamesSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://bans-api.cosmic.games/prisons/player/" + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        json_response = json.loads(response.text)
        if len(json_response) != 0:
            for offence in json_response:
                if offence['type'].lower() == 'ban'.lower():
                    ban_reason = offence['reason']
                    yield BanItem({
                        'source': tldextract.extract(response.url).domain,
                        'url': response.url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': int(offence['time'] / 1000),
                        'expires': 'Permanent' if offence['expiration'] == 0 else int(offence['expiration'] / 1000)
                    })