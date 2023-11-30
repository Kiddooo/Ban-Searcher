from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract
from datetime import datetime

class SnapcraftHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')
        bans = []

        table = soup.find('div', class_='ndzn-litebans-table')
        if table is not None:
            ban = {
                'source': tldextract.extract(url).domain,
                'url': url,
                'reason': table.find('div', class_='td _reason').text.strip(),
                'date': int(datetime.strptime(table.find('div', class_='td _date').text.strip(), "%B %d, %Y, %H:%M").timestamp()),
                'expires': int(datetime.strptime(table.find('div', class_='td _expires').text.replace("(Expired)", "").strip(), "%B %d, %Y, %H:%M").timestamp())
            }
            bans.append(ban)
        return bans