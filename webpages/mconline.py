import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import traceback
import json

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
async def parse_website_html(response_text):
    try:
        bans = []
        _ban = response_text.split("\n")[3:-1][0].split(';')
        ban = {
            'bannedby': _ban[0],
            'timebanned': _ban[1],
            'banreason': _ban[2]
        }
        bans.append(ban)
    except IndexError:
        pass
    
    return bans

async def handle_request(url, session):
    try:
        print(url)
        async with session.get(url,headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                bans = await parse_website_html(await response.text())
                return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
    except aiohttp.client.ClientConnectorError as e:
        print(traceback.format_exc() + url)