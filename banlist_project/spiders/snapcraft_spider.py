import dateparser
import scrapy
from bs4 import BeautifulSoup
import tldextract
from banlist_project.items import BanItem
from utils import get_language, translate

class SnapcraftSpider(scrapy.Spider):
    # Define the name of the spider
    name = 'SnapcraftSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        # Initialize the spider with the player's username and UUIDs
        super(SnapcraftSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        # Define the URLs to scrape
        urls = [
            f"https://snapcraft.net/bans/search/{self.player_username}/?filter=bans",
            f"https://www.mcfoxcraft.com/bans/search/{self.player_username}/?filter=bans"
        ]
        # Start the requests for each URL
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        # Find the table with the ban data
        table = soup.find('div', class_='ndzn-litebans-table')
        if table is not None:
            # Get all the rows in the table
            rows = table.find_all('div', class_='row')
            for row in rows:
                # Extract the ban date and handle any exceptions
                ban_date = self.get_ban_date(row)
                # Extract the ban expiry and handle any exceptions
                ban_expires = self.get_ban_expiry(row)
                # Extract the ban reason
                ban_reason = row.find('div', class_='td _reason').text.strip()
                # Yield a new BanItem with the extracted data
                yield BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': ban_date,
                    'expires': ban_expires
                })

    def get_ban_date(self, row):
        # Try to parse the ban date from the row
        try:
            ban_date = int(dateparser.parse(row.find('div', class_='td _date').text.strip()).timestamp())
        except ValueError:
            # If parsing fails, log an error and continue
            print("Failed to parse ban date:", row.find('div', class_='td _date').text.strip())
            ban_date = 'N/A'
        return ban_date

    def get_ban_expiry(self, row):
        # Try to parse the ban expiry from the row
        ban_expires = row.find('div', class_='td _expires').text.strip().split(" (")[0]
        if ban_expires == 'Expired':
            ban_expires = 'N/A'
        elif ban_expires == 'Permanent Ban':
            ban_expires = 'Permanent'
        else:
            try:
                ban_expires = int(dateparser.parse(ban_expires).timestamp())
            except ValueError:
                # If parsing fails, log an error and continue
                print("Failed to parse ban expiry:", ban_expires)
                ban_expires = 'N/A'
        return ban_expires