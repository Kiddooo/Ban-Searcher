from datetime import datetime
from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract

class DemocracycraftHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')
        bans = []

        table = soup.find('table', class_='results')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')[1:]
                expires_date_object = 'Permanent' if columns[3].text.strip() == 'Never' else  int(datetime.strptime(columns[3].text.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%m/%d/%Y %I:%M %p").timestamp())
                ban_date_object = int(datetime.strptime(columns[2].text.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%m/%d/%Y %I:%M %p").timestamp())

                ban = {
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': columns[1].text,
                    'date': ban_date_object,
                    'expires': expires_date_object
                }
                bans.append(ban)
        return bans