import re
import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import tldextract
from utils import get_language, translate

class ManaCubeSpider(scrapy.Spider):
    name = 'ManaCubeSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(ManaCubeSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://manacube.com/members/" + self.player_username + ".html"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        bans_tab = soup.find_all('div', class_='tab-pane', id='bans')
        table = bans_tab[0].find('table', class_='table table-striped table-profile')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')[1:]
                expires_date_object = int(datetime.strptime(columns[4].text.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%d %B %Y at %I:%M%p").replace(tzinfo=timezone.utc).timestamp())
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import tldextract
from utils import get_language, translate

class ManaCubeSpider(scrapy.Spider):
    name = 'ManaCubeSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(ManaCubeSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://bans.manacube.com/user?user=" + self.player_username + "#bans"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        bans_tab = soup.find_all('div', class_='tab-pane', id='bans')
        table = bans_tab[0].find('table', class_='table table-striped table-profile')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                
                columns = row.find_all('td')[1:]
                
                expires_date_string = columns[4].text.replace('at', '')
                expires_date_string = re.sub(r'(\d)(st|nd|rd|th)', r'\1', expires_date_string)
                expires_date_string = ' '.join(expires_date_string.split())
                expires_date_object = int(dateparser.parse(expires_date_string).replace(tzinfo=timezone.utc).timestamp())
                
                ban_date_string = columns[3].text.replace('at', '')
                ban_date_string = re.sub(r'(\d)(st|nd|rd|th)', r'\1', ban_date_string)
                ban_date_string = ' '.join(ban_date_string.split())
                ban_date_object = int(dateparser.parse(ban_date_string).replace(tzinfo=timezone.utc).timestamp())
                
                ban_reason = columns[0].text
                
                yield BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': ban_date_object,
                    'expires': expires_date_object
                })