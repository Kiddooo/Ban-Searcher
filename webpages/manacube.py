
import requests
from bs4 import BeautifulSoup
import traceback
from utils import USER_AGENT
import tldextract
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

def parse_website_html(response_text, url):
    soup = BeautifulSoup(response_text, 'html.parser')

    bans = []

    bans_tab = soup.find_all('div', class_='tab-pane', id='bans')
    table = bans_tab[0].find('table', class_='table table-striped table-profile')
    if table is not None:
        for row in table.find_all('tr')[1:]: # Skip the header row
            columns = row.find_all('td')[1:]
            expires_date_object = int(datetime.strptime(columns[4].text.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%d %B %Y at %I:%M%p").replace(tzinfo=timezone.utc).timestamp())
            ban_date_object = int(datetime.strptime(columns[3].text.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%d %B %Y at %I:%M%p").replace(tzinfo=timezone.utc).timestamp())
            
            ban = {
                'source': tldextract.extract(url).domain,
                'url': url,
                'reason': columns[0].text,
                'date': ban_date_object,
                'expires': expires_date_object
            }
            bans.append(ban)
    return bans

def handle_request(url):
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        if response.status_code == 200:
            bans = parse_website_html(response.text, url)
            return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
    except requests.exceptions.RequestException:
        print(traceback.format_exc() + url)
