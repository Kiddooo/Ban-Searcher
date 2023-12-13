from datetime import datetime
import json
import scrapy
import tldextract
from banlist_project.items import BanItem
from utils import get_language, translate

# Constants
BASE_URL = "https://mccentral.org/punishments/resources/api/bans.php?uuid="

class MCCentralSpider(scrapy.Spider):
    name = 'MCCentralSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MCCentralSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        # Construct the URL using f-string for better readability
        url = f"{BASE_URL}{self.player_uuid}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Parse the JSON response
        json_response = json.loads(response.text)['results']

        # Check if there are any offences
        if json_response['offence_count'] != 0:
            # Iterate over the offences
            for offence in json_response['offences']:
                if offence['severity'] in ['1', '3'] and offence['timeleft'] != 'Appealed':
                    ban_reason = offence['reason']
                    domain = tldextract.extract(response.url).domain
                    # Yield a BanItem for each offence
                    yield BanItem({
                        'source': domain,
                        'url': response.url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': int(datetime.strptime(offence['datetime'].replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%d %B %Y").timestamp()),
                        'expires': "Permanent" if offence['timeleft'] == "Forever" else "N/A"
                    })