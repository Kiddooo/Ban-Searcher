from bs4 import BeautifulSoup
from urllib.parse import urljoin
from WebsiteBaseHandler import BaseHandler
import tldextract
import datetime
import requests

from utils import get_language, translate

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class MCBansHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        if response_text == "":
            return []

        soup = BeautifulSoup(response_text, 'html.parser')

        bans = []

        while True:
            table = soup.find_all('table', class_='i-table fullwidth')[1]
            if table is not None:
                for row in table.find_all('tr')[1:-1]: # Skip the header row
                    columns = row.find_all('td')[:-1]
                    ban_reason = columns[4].text
                    ban = {
                        'source': tldextract.extract(url).domain,
                        'url': url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': int(datetime.datetime.strptime(columns[5].text, DATE_FORMAT).timestamp()),
                        'expires': 'N/A'
                    }
                    bans.append(ban)

            pagination_link = soup.find('span', class_='fa fa-step-forward')
            if 'disabled' in pagination_link.parent.get('class'):
                # No more pages
                break
            else:
                next_page_url = urljoin(url, pagination_link.parent['href'])
                response = requests.get(next_page_url, timeout=60)
                soup = BeautifulSoup(response.text, 'html.parser')

        return bans