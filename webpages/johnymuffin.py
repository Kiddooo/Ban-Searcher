from bs4 import BeautifulSoup, Comment
from WebsiteBaseHandler import BaseHandler
import tldextract
import datetime

from utils import get_language, translate

DATE_FORMAT = "%b %d, %Y %I:%M:%S %p"


class JohnyMuffinHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')

        if soup.find('strong', text='Unknown User'):
            return None

        bans = []

        if soup.find(text=lambda text: isinstance(text, Comment) and 'user.ban_received_table_start' in text):
            table = soup.find_all('table', class_='table table-bordered')[0]
            if table is not None:
                for row in table.find_all('tr')[1:]: # Skip the header row
                    columns = row.find_all('td')
                    ban_reason = columns[2].text
                    ban = {
                        'source': tldextract.extract(url).domain,
                        'url': url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': "N/A",
                        'expires': "Permanent" if "Permanent" in columns[3].text else int(datetime.datetime.strptime(columns[3].text, DATE_FORMAT).timestamp())
                    }
                    bans.append(ban)
            return bans