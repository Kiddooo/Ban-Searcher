import dateparser
import scrapy
from bs4 import BeautifulSoup
import tldextract
from banlist_project.items import BanItem
from utils import get_language, translate

# Constants for better readability
HEADER_ROW_INDEX = 1

class SyuuSpider(scrapy.Spider):
    name = 'SyuuSpider'

    # Initialize spider with player details
    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(SyuuSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    # Start requests for the spider
    def start_requests(self):
        # Construct the URL with player UUID
        url = f"https://www.syuu.net/user/{self.player_uuid_dash}"
        # Make a request to the URL and call the parse function when the request is completed
        yield scrapy.Request(url, callback=self.parse, meta={'flare_solver': True})

    # Parse the response from the request
    def parse(self, response):
        # Parse the HTML response using BeautifulSoup
        parsed_html = BeautifulSoup(response.text, 'lxml')
        # Find the punishment table in the parsed HTML
        punishment_table = parsed_html.find('table', id='punishment-table', class_='table table-bordered')
        # If the punishment table is found
        if punishment_table is not None:
            # Get all rows in the table, skipping the header row
            rows = punishment_table.find_all('tr')[HEADER_ROW_INDEX:]
            # Process each row
            for row in rows:
                # Skip rows with a class attribute
                if row.get('class'):
                    continue
                # If the row represents a ban
                if row.find('div').text.lower() == 'ban':
                    # Get all columns in the row
                    columns = row.find_all('td')[1:]
                    # Get the URL of the ban
                    ban_url = response.urljoin(columns[0].find('a')['href'])
                    # Make a request to the ban URL and call the parse_ban function when the request is completed
                    yield scrapy.Request(ban_url, callback=self.parse_ban, meta={'flare_solver': True})

    # Parse the response from the ban request
    def parse_ban(self, response):
        # Parse the HTML response using BeautifulSoup
        parsed_html = BeautifulSoup(response.text, 'lxml')
        # Find the ban details table in the parsed HTML
        ban_details_table = parsed_html.find('table', class_='table table-striped')
        # If the ban details table is found
        if ban_details_table is not None:
            # Get all rows in the table, skipping the header row
            rows = ban_details_table.find_all('tr')[HEADER_ROW_INDEX:]
            # Get the ban reason
            ban_reason = rows[0].find_all('td')[1].text
            # Yield a BanItem with the ban details
            yield BanItem({
                'source': tldextract.extract(response.url).domain,
                'url': response.url,
                'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                'date': int(dateparser.parse(rows[2].find_all('td')[1].text).timestamp()),
                'expires': int(dateparser.parse(rows[3].find_all('td')[1].text).timestamp())
            })