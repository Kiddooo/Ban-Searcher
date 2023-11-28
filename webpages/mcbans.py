from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from utils import USER_AGENT
import tldextract
import datetime
import requests

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def parse_website_html(response_text, url):
    if response_text == "":
        return []
    
    soup = BeautifulSoup(response_text, 'html.parser')

    bans = []

    while True:
        table = soup.find_all('table', class_='i-table fullwidth')[1]
        if table is not None:
            for row in table.find_all('tr')[1:-1]: # Skip the header row
                columns = row.find_all('td')[:-1]
                ban = {
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': columns[4].text,
                    'date': int(datetime.datetime.strptime(columns[5].text, DATE_FORMAT).timestamp()),
                    'expires': 'N/A'    
                }
                bans.append(ban)

        pagination_link = soup.find('span', class_='fa fa-step-forward')
        if 'disabled' in pagination_link.parent.get('class'):
            # No more pages
            break
        else:
            next_page_url = urljoin(url, pagination_link.parent['href'])
            response = requests.get(next_page_url)
            soup = BeautifulSoup(response.text, 'html.parser')

    return bans


def handle_request(url):
    try:
        tqdm.write(f"Fetching {url}...")
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        if response.status_code == 200:
            bans = parse_website_html(response.text, url)
            return bans
    except requests.exceptions.RequestException as e:
        print(str(e) + url)