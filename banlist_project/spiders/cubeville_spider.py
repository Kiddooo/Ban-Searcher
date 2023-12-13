import scrapy
from banlist_project.items import BanItem
import dateparser
import tldextract
from bs4 import BeautifulSoup
from utils import get_language, translate

# Define constants
PERMANENT = "permanent"

class CubevilleSpider(scrapy.Spider):
    """Spider for Cubeville"""
    name = 'CubevilleSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        """Initialize spider with username and UUIDs"""
        super(CubevilleSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        """
        Start requests by constructing URL with username.
        This function is called by Scrapy when the spider is opened.
        """
        url = "https://www.cubeville.org/cv-site/banlist.php/" + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse response from request.
        This function is called by Scrapy with the response of the request made in start_requests.
        """
        # Parse the response text with BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")
        # Find all tables in the parsed HTML
        table = soup.find_all("table")
        # Iterate over each row in the first table, skipping the header row
        for row in table[0].find_all("tr")[1:]:
            # Find all columns in the row
            columns = row.find_all("td")
            # If the first column matches the player username
            if columns[0].text == self.player_username:
                # Parse the ban date
                banned_at = dateparser.parse(columns[1].text)
                # Get the ban duration text
                ban_duration_text = columns[3].text.strip()
                # Calculate the ban expiration date
                ban_expires = self.get_ban_expires(ban_duration_text, banned_at)
                # Get the ban reason
                ban_reason = columns[2].text
                # Yield a BanItem for each ban
                yield self.create_ban_item(response, ban_reason, banned_at, ban_expires)

    def get_ban_expires(self, ban_duration_text, banned_at):
        """
        Calculate ban expiration date.
        If the ban is permanent, return "Permanent".
        Otherwise, parse the ban duration text to calculate the expiration date.
        """
        if ban_duration_text == PERMANENT:
            return "Permanent"
        else:
            return int(dateparser.parse(f"in {ban_duration_text}", settings={"RELATIVE_BASE": banned_at}).timestamp())

    def create_ban_item(self, response, ban_reason, banned_at, ban_expires):
        """
        Create and return a BanItem.
        A BanItem includes the source, URL, reason, date, and expiration of the ban.
        """
        return BanItem({
            'source': tldextract.extract(response.url).domain,
            'url': response.url,
            'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
            'date': int(banned_at.timestamp()),
            'expires': ban_expires,
        })