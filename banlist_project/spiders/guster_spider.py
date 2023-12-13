import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
from utils import get_language, translate
from urllib.parse import urlparse
import json

# Constants
BASE_URL = "https://bans.guster.ro/api.php?type=player&player={}&page={}&perpage=25"

class GusterSpider(scrapy.Spider):
    name = 'GusterSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(GusterSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        # Format the URL with the player's username
        url = BASE_URL.format(self.player_username, 1)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Load the response text as JSON
        banlist = json.loads(response.text)
        last_page = banlist['lastpage']

        # If there are no punishments, return
        if banlist['totalpunish'] == '0':
            return

        # Loop through all pages and send a request for each
        for page in range(1, last_page + 1):
            yield scrapy.Request(BASE_URL.format(self.player_username, page), callback=self.parse_page)

    def parse_page(self, response):
        # Load the ban list from the response
        bans_on_page = json.loads(response.text)['banlist']

        # Loop through all bans on the page
        for ban in bans_on_page:
            # If the ban is a dictionary and contains all necessary keys
            if isinstance(ban, dict) and 'Ban' in ban.get('type') and all(key in ban for key in ['reason', 'date', 'expire']):
                # Yield a new BanItem
                yield BanItem({
                    'source': urlparse(response.url).hostname,
                    'reason': translate(ban['reason']) if get_language(ban['reason']) != 'en' else ban['reason'],
                    'url': response.url,
                    'date': int(dateparser.parse(BeautifulSoup(ban['date'], 'lxml').text).timestamp()),
                    'expires': 'Permanant' if 'Never' in ban['expire'] else 'N/A' if 'Expired' in ban['expire'] else int(dateparser.parse(BeautifulSoup(ban['expire'], 'lxml').text).timestamp())
                })