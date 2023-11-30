from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract
import datetime

PLAYER_DOESNT_EXIST = "Player doesn't exist"
NO_BANS = "No bans have been filed."
NO_PERM_BANS = "No permanent bans have been filed."
NO_AUTO_BANS = "No automatic bans have been filed."

class MCBrawlHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        bans = []
        for ban_type in ['bans', 'permbans', 'autobans']:
            soup = BeautifulSoup(response_text, 'html.parser')

            if soup.find('div', class_='alert alert-danger text-center'):
                if PLAYER_DOESNT_EXIST in soup.find('div', class_='alert alert-danger text-center').text:
                    return []

            ban_element = soup.find_all('div', class_='tab-pane', id=ban_type)

            if ban_type not in ban_element[0].text:
                table = ban_element[0].find('table', class_='table table-striped table-condensed')
                if table is not None:
                    for row in table.find_all('tr')[1:]: # Skip the header row
                        columns = row.find_all('td')
                        ban = {
                            'source': tldextract.extract(url).domain,
                            'url': url,
                            'reason': columns[0].text,
                            'date': int(datetime.datetime.strptime(columns[1].text, "%Y-%m-%d %H:%M:%S").timestamp()),
                            'expires': 'N/A' if columns[2].text == "" else int(datetime.datetime.strptime(columns[2].text, "%Y-%m-%d %H:%M:%S").timestamp()),
                        }
                        bans.append(ban)
        return bans
