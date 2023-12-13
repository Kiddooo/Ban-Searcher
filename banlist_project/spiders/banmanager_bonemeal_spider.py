import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from utils import get_language, translate

class BanManagerBonemealSpider(scrapy.Spider):
    name = 'BanManagerBonemealSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(BanManagerBonemealSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://mineyourmind.net/bans/index.php/players/" + self.player_uuid
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        # Find all timeline items
        timeline_items = soup.find_all('li', class_='timeline')

        # Find all inverted timeline items (for the second "pvp bypass" ban)
        timeline_inverted_items = soup.find_all('li', class_='timeline-inverted')

        # Combine both lists
        all_items = timeline_items + timeline_inverted_items

        for item in all_items:
            ban_reason = item.find('div', class_='timeline-body').get_text().split("\n")[1].strip().split(":")[1].strip()
            try:
                
            # Get ban date
                ban_date_str = soup.find('small', class_='text-muted')['title']
                ban_date = dateparser.parse(ban_date_str)
            except ValueError:
                ban_date = "N/A"
                
            ban_start_date_str = item.find('small', class_='text-muted')['title']
            ban_start_date = dateparser.parse(ban_start_date_str)

                # Check if the ban is permanent
            if '(permanent)' in item.find('div', class_='timeline-body').get_text(strip=True).lower():
                ban_end_timestamp = 'Permanent'
            else:
                # Get ban length
                ban_length_str = re.search(r'Lasted for (\d+ \w+).', item.find('div', class_='timeline-body').get_text(strip=True))
                if ban_length_str:
                    ban_length_str = ban_length_str.group(1)
                    ban_length = dateparser.parse('in ' + ban_length_str) - dateparser.parse('now')

                    # Calculate ban end date
                    ban_end_date = ban_start_date + ban_length

                    # Convert the ban end date to a Unix timestamp
                    ban_end_timestamp = int(ban_end_date.timestamp())
                else:
                    ban_end_timestamp = 'N/A'
                
            yield BanItem({
                'source': 'bonemeal',
                'url': response.url,
                'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                'date': int(ban_date.timestamp()),
                'expires': ban_end_timestamp
            })
            
            
# https://mineyourmind.net/bans/index.php/players/b53f314d5872449c9eb3979e5e4a0ce7
# https://mineyourmind.net/bans/index.php/players/79a1584f109e4fc3a42fe3f00fb7007f