import dateparser
import scrapy
from bs4 import BeautifulSoup
import tldextract
from banlist_project.items import BanItem
from utils import get_language, translate

# Constants
PLAYER_DOESNT_EXIST = "Player doesn't exist"
NO_BANS = "No bans have been filed."
NO_PERM_BANS = "No permanent bans have been filed."
NO_AUTO_BANS = "No automatic bans have been filed."
BASE_URL = "https://www.mcbrawl.com/history/player/"

class MCBrawlSpider(scrapy.Spider):
    name = 'MCBrawlSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MCBrawlSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        # Construct the URL using the base URL and the player's username
        url = BASE_URL + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Create a BeautifulSoup object once before the loop
        soup = BeautifulSoup(response.text, 'lxml')

        # Check if player exists
        player_exists_div = soup.find('div', class_='alert alert-danger text-center')
        if player_exists_div and PLAYER_DOESNT_EXIST in player_exists_div.text:
            return

        # Loop through different types of bans
        for ban_type in ['bans', 'permbans', 'autobans']:
            ban_elements = soup.find_all('div', class_='tab-pane', id=ban_type)

            # Check if ban type exists in the text
            if ban_type not in ban_elements[0].text:
                ban_table = ban_elements[0].find('table', class_='table table-striped table-condensed')

                # If table exists, process each row (skip the header)
                if ban_table is not None:
                    for row in ban_table.find_all('tr')[1:]:
                        columns = row.find_all('td')
                        ban_reason = columns[0].text

                        # Get language of the ban reason
                        try:
                            ban_reason_lang = get_language(ban_reason)
                        except IndexError:
                            ban_reason_lang = 'en'

                        # Yield a BanItem for each ban
                        yield BanItem({
                            'source': tldextract.extract(response.url).domain,
                            'url': response.url,
                            'reason': translate(ban_reason) if ban_reason_lang != 'en' else ban_reason,
                            'date': int(dateparser.parse(columns[1].text).timestamp()),
                            'expires': 'N/A' if columns[2].text == "" else int(dateparser.parse(columns[2].text).timestamp()),
                        })