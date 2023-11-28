import requests
from bs4 import BeautifulSoup
import traceback
from utils import USER_AGENT
from urllib.parse import urlparse
from datetime import datetime
import json
from tqdm import tqdm


def fetch_page(base_url, player_name, page):
    response = requests.get(base_url.format(player_name, page), headers={"User-Agent": USER_AGENT})
    if response.status_code == 200:
        data = response.json()
        return data['banlist']
    else:
        raise Exception(f"Failed to fetch page {page} with status {response.status_code}")

def parse_website_html(response_text, url):
    banlist = json.loads(response_text)
    last_page = banlist['lastpage']
    if banlist['totalpunish'] == '0':
        return None

    bans = []
    player_name: str = url.split("&")[1].split("=")[1]
    base_url: str = url.split('?')[0] + "?type=player&player={}&page={}&perpage=25"

    _bans_list = [requests.get(base_url.format(player_name, page), headers={"User-Agent": USER_AGENT}).json() for page in range(1, last_page + 1)]
    
    bans = [
    {
        'source': urlparse(url).hostname,
        'reason': ban['reason'],
        'url': url,
        'date': int(datetime.strptime(BeautifulSoup(ban['date'], 'html.parser').text, "%H:%M:%S %d.%m.%Y").timestamp()),
        'expires': 'Permanant' if 'Never' in ban['expire'] else 'N/A' if 'Expired' in ban['expire'] else int(datetime.strptime(BeautifulSoup(ban['expire'], 'html.parser').text, "%H:%M:%S %d.%m.%Y").timestamp())
    }
    for ban_list in _bans_list
    for ban in ban_list
    if isinstance(ban, dict) and 'Ban' in ban.get('type') and all(key in ban for key in ['reason', 'date', 'expire'])
    ]

    return bans

def handle_request(url):
    try:
        tqdm.write(f"Fetching {url}...")
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        if response.status_code == 200:
            bans = parse_website_html(response.text, url)
            return bans
    except AttributeError:
        pass
    except requests.exceptions.RequestException:
        pass