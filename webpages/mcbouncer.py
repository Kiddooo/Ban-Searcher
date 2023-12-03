from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import tldextract
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from WebsiteBaseHandler import BaseHandler
from utils import get_language, translate

class MCBouncerHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')

        bans = []

        while True:
            table = soup.find('table')
            if table is not None:
                for row in table.find_all('tr')[1:]:  # Skip the header row
                    columns = row.find_all('td')

                    website_ban_date_years = columns[2].text.replace('\xa0', " ").split("year")[0].strip()
                    website_ban_date_months = columns[2].text.replace("\xa0", "", ).split("month")[0].split(",")[1].replace("ago", "").strip()
                    now = date.today()
                    ban_date = datetime.combine(now - relativedelta(years=int(website_ban_date_years), months=int(website_ban_date_months)), datetime.min.time())
                    ban_reason = columns[1].text
                    ban = {
                        'source': tldextract.extract(url).domain,
                        'url': url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': int(ban_date.timestamp()),
                        'expires': 'N/A'
                    }
                    bans.append(ban)

            # Find the "Next" button and its parent li element
            next_button = soup.find('a', string='»')
            if next_button is not None:
                next_button_parent = next_button.find_parent('li')

                # If the parent li element has the "disabled" class, it means that there are no more pages
                if 'disabled' in next_button_parent.get('class', []):
                    break

                # Join the base URL with the href of the next page to get the full URL of the next page
                next_page_url = urljoin(url, next_button['href'])

                # Send a GET request to the next page
                response = requests.get(next_page_url, timeout=60)
                soup = BeautifulSoup(response.text, 'html.parser')

        return bans