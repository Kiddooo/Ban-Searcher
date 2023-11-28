import aiohttp
import json
import traceback
from utils import USER_AGENT
import tldextract
from datetime import datetime
import requests

def parse_website_html(response_text, url):
    bans = []
    json_response = json.loads(response_text)['results']
    
    if json_response['offence_count'] != 0:
        for offence in json_response['offences']:
            if offence['timeleft'] != 'Appealed':
                bans.append({
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': offence['reason'],
                    'date': int(datetime.strptime(offence['datetime'].replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%d %B %Y").timestamp()),
                    'expires': "Permanent" if offence['timeleft'] == "Forever" else "N/A"
                })
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