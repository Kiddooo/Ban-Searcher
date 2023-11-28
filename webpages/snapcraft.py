# https://snapcraft.net/bans/search/TheLionTR/
from bs4 import BeautifulSoup
from utils import USER_AGENT
import tldextract
from datetime import datetime
import requests

def parse_website_html(response_text, url):
    soup = BeautifulSoup(response_text, 'html.parser')
    bans = []

    table = soup.find('div', class_='ndzn-litebans-table')
    if table is not None:
        ban = {
            'source': tldextract.extract(url).domain,
            'url': url,
            'reason': table.find('div', class_='td _reason').text.strip(),
            'date': int(datetime.strptime(table.find('div', class_='td _date').text.strip(), "%B %d, %Y, %H:%M").timestamp()),
            'expires': int(datetime.strptime(table.find('div', class_='td _expires').text.replace("(Expired)", "").strip(), "%B %d, %Y, %H:%M").timestamp())
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
    except requests.exceptions.RequestException as e:
        print(str(e) + url)