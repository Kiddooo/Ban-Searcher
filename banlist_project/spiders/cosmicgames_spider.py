import scrapy
from banlist_project.items import BanItem
import json
import tldextract
from utils import get_language, translate

# Define constants for static values
BASE_URL = "https://bans-api.cosmic.games/prisons/player/"

class CosmicGamesSpider(scrapy.Spider):
    name = 'CosmicGamesSpider'

    # Initialize spider with username and UUIDs
    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(CosmicGamesSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    # Start requests by constructing URL with username
    def start_requests(self):
        url = f"{BASE_URL}{self.player_username}"
        yield scrapy.Request(url, callback=self.parse)

    # Parse response from request
    def parse(self, response):
        # Handle potential JSON decoding errors
        try:
            json_response = json.loads(response.text)
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return

        # If response is not empty, process each offence
        if len(json_response) != 0:
            for offence in json_response:
                # Only process 'ban' offences
                if offence['type'].lower() == 'ban'.lower():
                    ban_reason = offence['reason']
                    # Yield a BanItem for each offence, translating reason if not in English
                    yield BanItem({
                        'source': tldextract.extract(response.url).domain,
                        'url': response.url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': int(offence['time'] / 1000),
                        'expires': 'Permanent' if offence['expiration'] == 0 else int(offence['expiration'] / 1000)
                    })