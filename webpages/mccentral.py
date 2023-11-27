import aiohttp
import json
import traceback
from utils import USER_AGENT
import tldextract
from datetime import datetime

async def parse_website_html(response_text, url):
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

async def handle_request(url, session):
    try:
        print(f"Fetching {url}...")
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                bans = await parse_website_html(await response.text(), url)
                return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
    except aiohttp.client.ClientConnectorError:
        print(traceback.format_exc() + url)