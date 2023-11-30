
from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract


class CultcraftHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')

        bans = []

        table = soup.find('table', id='banlist', class_='table-hover')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')[1:]
                expires_date_object = 'Permanent' if columns[3].text.strip() == 'Permaban' else columns[3].text
                ban_date_object = 'N/A' if columns[2].text.strip() == 'Permanent (für immer)' else columns[2].text

                ban = {
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': columns[0].text,
                    'date': ban_date_object,
                    'expires': expires_date_object
                }
                bans.append(ban)
        return bans