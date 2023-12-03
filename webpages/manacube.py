from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract
from datetime import datetime, timezone

from utils import get_language, translate


class ManaCubeHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')

        bans = []

        bans_tab = soup.find_all('div', class_='tab-pane', id='bans')
        table = bans_tab[0].find('table', class_='table table-striped table-profile')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')[1:]
                expires_date_object = int(datetime.strptime(columns[4].text.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%d %B %Y at %I:%M%p").replace(tzinfo=timezone.utc).timestamp())
                ban_date_object = int(datetime.strptime(columns[3].text.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%d %B %Y at %I:%M%p").replace(tzinfo=timezone.utc).timestamp())
                ban_reason = columns[0].text
                ban = {
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                    'date': ban_date_object,
                    'expires': expires_date_object
                }
                bans.append(ban)
        return bans