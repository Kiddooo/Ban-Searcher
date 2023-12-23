import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
import re
from utils import get_language, translate, logger

# Define constants for repeated string values
TIMELINE = 'timeline'
TIMELINE_INVERTED = 'timeline-inverted'
TEXT_MUTED = 'text-muted'
PERMANENT = '(permanent)'

# Spider class
class BanManagerBonemealSpider(scrapy.Spider):
    name = 'BanManagerBonemealSpider'

    # Constructor
    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(BanManagerBonemealSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    # Function to start requests
    def start_requests(self):
        url = "https://mineyourmind.net/bans/index.php/players/" + self.player_uuid
        yield scrapy.Request(url, callback=self.parse)

    # Function to parse the response
    def parse(self, response):
        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'lxml')

        # Find all timeline and inverted timeline items
        timeline_items = soup.find_all('li', class_=TIMELINE)
        timeline_inverted_items = soup.find_all('li', class_=TIMELINE_INVERTED)

        # Combine both lists
        all_timeline_items = timeline_items + timeline_inverted_items

        # Iterate over all timeline items
        for item in all_timeline_items:
            # Extract ban reason
            ban_reason = item.find('div', class_='timeline-body').get_text().split("\n")[1].strip().split(":")[1].strip()

            # Parse the ban date and calculate the timestamp
            ban_date_str = soup.find('small', class_=TEXT_MUTED)['title']
            ban_date = self.parse_date(ban_date_str)
            ban_date_timestamp = self.calculate_timestamp(ban_date)

            # Extract ban start date
            ban_start_date_str = item.find('small', class_=TEXT_MUTED)['title']
            ban_start_date = self.parse_date(ban_start_date_str)

            # Check if the ban is permanent
            if PERMANENT in item.find('div', class_='timeline-body').get_text(strip=True).lower():
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
                    ban_end_timestamp = self.calculate_timestamp(ban_end_date)
                else:
                    ban_end_timestamp = 'N/A'

            # Yield a BanItem
            yield BanItem({
                'source': 'bonemeal',
                'url': response.url,
                'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                'date': ban_date_timestamp,
                'expires': ban_end_timestamp
            })
            
        # Function to parse date strings and handle errors
    def parse_date(self, date_str):
        try:
            return dateparser.parse(date_str)
        except ValueError:
            logger.error(f"Error parsing date: {date_str}")
            return None

    # Function to calculate timestamps from dates
    def calculate_timestamp(self, date):
        if date is not None:
            return int(date.timestamp())
        else:
            return 'N/A'