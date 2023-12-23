import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
import dateparser
from banlist_project.items import BanItem
from utils import get_language, translate

BASE_URL = "https://mcbouncer.com/u/{}/bansFor"

class MCBouncerSpider(scrapy.Spider):
    name = 'MCBouncerSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MCBouncerSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = BASE_URL.format(self.player_uuid)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        parsed_html = BeautifulSoup(response.text, 'lxml')

        while True:
            self.parse_table(parsed_html, response)

            # Find the "Next" button and its parent li element
            next_button = parsed_html.find('a', string='»')
            if next_button is not None:
                next_button_parent = next_button.find_parent('li')

                # If the parent li element has the "disabled" class, it means that there are no more pages
                if 'disabled' in next_button_parent.get('class', []):
                    break

                # Join the base URL with the href of the next page to get the full URL of the next page
                next_page_url = urljoin(response.url, next_button['href'])

                # Yield a new request to the next page
                yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_table(self, parsed_html, response):
        table = parsed_html.find('table')
        if table is not None:
            for row in table.find_all('tr')[1:]:  # Skip the header row
                columns = row.find_all('td')

                ban_reason = columns[1].text
                yield BanItem({
                    'source': tldextract.extract(response.url).domain,
                    'url': response.url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': int(dateparser.parse(columns[2].text.replace('\xa0', " ")).timestamp()),
                    'expires': 'N/A'
                })