from datetime import datetime
from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract
import urllib

from utils import get_language, translate

class SyuuHandler(BaseHandler):
    
    def handle_request(self, url):
        response_text = self.handle_flaresolverr_request(url)
        bans = self.parse_website_html(response_text, url)
        return bans
    
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')
        bans = []

        table = soup.find('table', id='punishment-table', class_='table table-bordered')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                if row.get('class'):
                    pass
                else:
                    if row.find('div').text.lower() == 'ban':
                        columns = row.find_all('td')[1:]
                        ban_url = self.handle_flaresolverr_request(urllib.parse.urljoin(url, columns[0].find('a')['href']))
                        soup2 = BeautifulSoup(ban_url, 'html.parser')
                        table2 = soup2.find('table', class_='table table-striped')
                        if table2 is not None:
                            row2 = table2.find_all('tr')[1:]
                            ban_reason = row2[0].find_all('td')[1].text
                            ban = {
                                'source': tldextract.extract(url).domain,
                                'url': url,
                                'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                                'date': int(datetime.strptime(row2[2].find_all('td')[1].text, '%Y-%m-%d %H:%M:%S %z').timestamp()),
                                'expires': int(datetime.strptime(row2[3].find_all('td')[1].text, '%Y-%m-%d %H:%M:%S %z').timestamp())
                            }
        
                            bans.append(ban)
        return bans