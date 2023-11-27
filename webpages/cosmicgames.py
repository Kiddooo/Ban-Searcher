import aiohttp
import json
import traceback
from utils import USER_AGENT
import tldextract

async def parse_website_html(response_text, url):
    json_response = json.loads(response_text)
    bans = []
    if len(json_response) != 0:
        for offence in json_response:
            if offence['type'].lower() == 'ban'.lower() :
                bans.append({
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': offence['reason'],
                    'date': int(offence['time'] / 1000),
                    'expires': int(offence['expiration'] / 1000)
                })
    return bans

async def handle_request(url, session):
    try:
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                bans = await parse_website_html(await response.text(), url)
                return bans
    except AttributeError:
        print(traceback.format_exc() + url)
    except aiohttp.client.ClientConnectorError:
        print(traceback.format_exc() + url)