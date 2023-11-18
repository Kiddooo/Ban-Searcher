import aiohttp
import json
import traceback
from utils import USER_AGENT

async def parse_website_html(response_text):
    json_response = json.loads(response_text)['results']
    
    if json_response['offence_count'] != 0:
        return json_response['offences']

async def handle_request(url, session):
    try:
        print(url)
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                bans = await parse_website_html(await response.text())
                return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
    except aiohttp.client.ClientConnectorError:
        print(traceback.format_exc() + url)