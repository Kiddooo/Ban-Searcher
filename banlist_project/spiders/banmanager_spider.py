# Import necessary libraries
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
import tldextract
import dateparser
from utils import get_language, translate
import unicodedata

# Define constants
URLS = [
    "http://mc.virtualgate.org/ban/index.php?action=viewplayer&player=<USERNAME>&server=0",
    "https://woodymc.de/BanManager/index.php?action=viewplayer&player=<USERNAME>&server=0",
    "https://bans.piratemc.com/index.php?action=viewplayer&player=<USERNAME>&server=0"
]

# Define BanManagerSpider class
class BanManagerSpider(scrapy.Spider):
    name = 'BanManagerSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(BanManagerSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        for url in URLS:
            url = url.replace("<USERNAME>", self.player_username)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        # Parse current ban
        current_ban = self.parse_current_ban(soup, response)
        if current_ban:
            yield current_ban

        # Parse previous bans
        previous_bans = self.parse_previous_bans(soup, response)
        for ban in previous_bans:
            yield ban

    def parse_current_ban(self, soup, response):
        current_ban_table = soup.find('table', id='current-ban')
        if current_ban_table is not None:
            if current_ban_table.find('tr').find('td').text != 'None':
                current_ban = {}
                for row in current_ban_table.find_all('tr'):
                    columns = row.find_all('td')
                    if len(columns) == 2:  # Ensure there are exactly 2 columns
                        current_ban[columns[0].text.replace(':', '').lower()] = columns[1].text

                # Format the current ban information
                current_ban = list(current_ban.items())
                # Get ban start date
                ban_start_date_str = current_ban[2][1]
                ban_start_date = dateparser.parse(ban_start_date_str)

                # Get ban length
                ban_length_str = unicodedata.normalize('NFC', current_ban[0][1])
                if ban_length_str != "Permanent" and ban_length_str.strip() != "Dich sehen wir nicht wieder =:o)":
                    ban_length = dateparser.parse('in ' + ban_length_str) - dateparser.parse('now')

                    # Calculate ban end date
                    ban_end_date = ban_start_date + ban_length

                    # Convert the ban end date to a Unix timestamp
                    ban_end_timestamp = int(ban_end_date.timestamp())
                else:
                    ban_end_timestamp = 'Permanent'

                return BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': current_ban[3][1],
                    'date':  int(dateparser.parse(current_ban[2][1]).timestamp()),
                    'expires': ban_end_timestamp
                })

    def parse_previous_bans(self, soup, response):
        previous_bans_table = soup.find('table', id='previous-bans')
        if previous_bans_table is not None:
            if previous_bans_table.find_all('tr')[1:][0].find('td').text != 'None':
                for row in previous_bans_table.find_all('tr')[1:]:  # Skip the header row
                    columns = row.find_all('td')
                    if len(columns) >= 7:  # Ensure there are at least 7 columns
                        ban_reason = columns[1].text
                        yield BanItem({
                            'source': tldextract.extract(response.url).domain,
                            'url': response.url,
                            'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                            'date': int(dateparser.parse(columns[3].text).timestamp()),
                            'expires': int(dateparser.parse(columns[6].text).timestamp())
                        })