# Import necessary libraries
import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
import tldextract
from utils import translate, get_language

# Define constants for static values
PERMANENT = "Permanent"
NEVER = "Nikdy"

# Define the spider class
class MajncraftSpider(scrapy.Spider):
    # Set the name of the spider
    name = 'MajncraftSpider'

    # Initialize the spider with necessary parameters
    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MajncraftSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    # Define the start requests for the spider
    def start_requests(self):
        # Construct the URL
        url = "https://server.majncraft.cz/player/" + self.player_username
        # Yield a scrapy request to the URL, with the parse method as the callback
        yield scrapy.Request(url, callback=self.parse)

    # Define the parse method that will process the response from the request
    def parse(self, response):
        # Parse the response text with BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        # Find the section with the list of bans
        ban_list_section = soup.find('section', class_='list list-ban')

        # If the ban list section is found
        if ban_list_section is not None:
            # Find all panels in the ban list section
            panels = ban_list_section.find_all('div', class_='panel')
            # For each panel
            for panel in panels:
                # Extract the ban details from the panel
                ban_item = self.extract_ban_details(panel, response)
                # Yield the ban item
                yield ban_item

    # Define a helper function to extract ban details from a panel
    def extract_ban_details(self, panel, response):
        """Extracts ban details from a panel"""
        # Find the row in the panel
        row = panel.find('div', class_='row')
        # Find all divs in the row, which contain the ban details
        ban_details = row.find_all('div')
        # Extract the ban reason, date, and expiration from the ban details
        ban_reason = ban_details[1].contents[3].strip()
        ban_date = ban_details[2].get_text().strip().split()[1]
        ban_date = ban_date[:-5] + ' ' + ban_date[-5:]
        expires = ban_details[3].get_text().strip().split()[1]

        # Return a BanItem with the extracted details
        return BanItem({
            'source': tldextract.extract(response.url).domain,
            'url': response.url,
            'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
            'date': int(dateparser.parse(ban_date).timestamp()),
            'expires': PERMANENT if expires == NEVER else int(dateparser.parse(expires).timestamp())
        })