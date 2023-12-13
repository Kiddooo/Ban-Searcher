import dateparser
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
from banlist_project.items import BanItem
from utils import get_language, translate

# Constants for class names and other strings
TABLE_CLASS = 'i-table fullwidth'
PAGINATION_CLASS = 'fa fa-step-forward'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class MCBansSpider(scrapy.Spider):
    name = 'MCBansSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MCBansSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://www.mcbans.com/player/" + self.player_uuid
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        while True:
            # Extract data from the table
            data = self.extract_data(soup)

            # Create BanItem for each row of data
            for row in data:
                yield self.create_item(row, response)

            # Check if there are more pages
            pagination_link = soup.find('span', class_=PAGINATION_CLASS)
            if 'disabled' in pagination_link.parent.get('class'):
                # No more pages
                break
            else:
                next_page_url = urljoin(response.url, pagination_link.parent['href'])
                yield scrapy.Request(next_page_url, callback=self.parse)

    def extract_data(self, soup):
        """Extract data from the table in the HTML."""
        table = soup.find_all('table', class_=TABLE_CLASS)[1]
        data = []
        if table is not None:
            for row in table.find_all('tr')[1:-1]: # Skip the header row
                columns = row.find_all('td')[:-1]
                ban_reason = columns[4].text
                data.append({
                    'reason': ban_reason,
                    'date': columns[5].text
                })
        return data

    def create_item(self, row, response):
        """Create a BanItem from a row of data."""
        reason = translate(row['reason']) if get_language(row['reason']) != 'en' else row['reason']
        date = int(dateparser.parse(row['date']).timestamp())
        return BanItem({
            'source': tldextract.extract(response.url).domain,
            'url': response.url,
            'reason': reason,
            'date': date,
            'expires': 'N/A'
        })