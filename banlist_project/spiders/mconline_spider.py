import scrapy
import tldextract
from banlist_project.items import BanItem
from utils import get_language, translate

# Constants
URL_TEMPLATE = "https://minecraftonline.com/cgi-bin/getplayerinfo?{}"

class MCOnlineSpider(scrapy.Spider):
    """
    A Scrapy Spider that scrapes player information from minecraftonline.com.
    """
    name = 'MCOnlineSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        """
        Initialize the spider with the player's username and UUIDs.
        """
        super(MCOnlineSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        """
        This method generates the initial request to scrape player information.
        """
        url = URL_TEMPLATE.format(self.player_username)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        This method parses the response from the server and yields a BanItem.
        """
        try:
            # Split the response text by line and semicolon
            _ban = response.text.split("\n")[3:-1][0].split(';')

            # Yield a new BanItem with the parsed information
            yield BanItem({
                'source': tldextract.extract(response.url).domain,
                'url': response.url,
                'date': int(_ban[1]),
                'reason': translate(_ban[2]) if get_language(_ban[2]) != 'en' else _ban[2],
                'expires': 'N/A'
            })
        except IndexError:
            # Log a message if an error occurs
            self.log("Error parsing response for player: {}".format(self.player_username))