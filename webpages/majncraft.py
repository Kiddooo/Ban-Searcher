from datetime import datetime
from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract

class MajncraftHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')
        bans = []

        table = soup.find('section', class_='list list-ban')
        if table is not None:
            panels = table.find_all('div', class_='panel')
            for panel in panels:
                row = panel.find('div', class_='row')
                cols = row.find_all('div')
                
                ban = {
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': cols[1].contents[3].strip(),
                    'issued': int(datetime.strptime(cols[2].contents[3].strip() + " " + cols[2].contents[5].strip(), "%d.%m.%Y %H:%M").timestamp()),
                    'expires': cols[3].text.split()[1] if ':' not in cols[3].text.split()[1] else int(datetime.strptime(cols[3].contents[3].strip() + " " + cols[3].contents[5].strip(), "%d.%m.%Y %H:%M").timestamp())
                }
                bans.append(ban)
        
        return bans