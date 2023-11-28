import json
import traceback
from utils import USER_AGENT
import tldextract
import requests
from tqdm import tqdm

def parse_website_html(response_text, url):
    json_response = json.loads(response_text)
    bans = []
    if len(json_response) != 0:
        for offence in json_response:
            if offence['type'].lower() == 'ban'.lower():
                bans.append({
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': offence['reason'],
                    'date': int(offence['time'] / 1000),
                    'expires': int(offence['expiration'] / 1000)
                })
    return bans

def handle_request(url):
    try:
        tqdm.write(f"Fetching {url}...")
        with requests.get(url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status_code == 200:
                bans = parse_website_html(response.text, url)
                return bans
    except AttributeError:
        print(traceback.format_exc() + url)
    except requests.exceptions.RequestException:
        print(traceback.format_exc() + url)
