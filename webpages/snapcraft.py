from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract
from datetime import datetime

from utils import get_language, translate

class SnapcraftHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')
        bans = []

        table = soup.find('div', class_='ndzn-litebans-table')
        if table is not None:
            rows = table.find_all('div', class_='row')
            for row in rows:
                try:
                    ban_date = int(datetime.strptime(row.find('div', class_='td _date').text.strip(), "%B %d, %Y, %H:%M").timestamp())
                except ValueError:
                    ban_date = int(datetime.strptime(row.find('div', class_='td _date').text.strip(), "%d/%m/%Y, %H:%M").timestamp())

                ban_expires = row.find('div', class_='td _expires').text.replace('(Expired)', '').strip()

                ban_reason = row.find('div', class_='td _reason').text.strip()
                ban = {
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': ban_date,
                    'expires': 'N/A' if ban_expires == 'Expired' else int(datetime.strptime(ban_expires, "%B %d, %Y, %H:%M").timestamp())
                }
                bans.append(ban)
        return bans