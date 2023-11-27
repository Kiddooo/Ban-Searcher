import aiohttp
from bs4 import BeautifulSoup
import traceback
from utils import USER_AGENT
import json
import asyncio
import tldextract
from datetime import datetime

async def fetch_page(session, base_url, player_name, page):
   """
   Fetches a specific page of data for a player from the given base URL.

   Args:
       session (aiohttp.ClientSession): The aiohttp session to use for the request.
       base_url (str): The base URL with placeholders for player name and page number.
       player_name (str): The name of the player.
       page (int): The page number to fetch.

   Returns:
       list: The banlist data from the fetched page.

   Raises:
       Exception: If the request fails with a non-200 status code.
   """
   async with session.get(base_url.format(player_name, page), headers={"User-Agent": USER_AGENT}) as response:
       if response.status == 200:
           data = json.loads(await response.text())
           return data['banlist']
       else:
           raise Exception(f"Failed to fetch page {page} with status {response.status}")

async def parse_website_html(response_text, session, url):
    """
    Parse the HTML of a website and extract ban information.

    Args:
        response_text (str): The HTML response text of the website.
        session (aiohttp.ClientSession): The aiohttp client session used for making HTTP requests.
        url (str): The URL of the website.

    Returns:
        List[Dict[str, Union[str, datetime.datetime]]]: A list of dictionaries representing the bans found on the website. Each dictionary contains the following keys:
            - 'source' (str): The domain of the website.
            - 'reason' (str): The reason for the ban.
            - 'url' (str): The URL of the banned page.
            - 'date' (str): The date the ban was issued.
            - 'expires' (str): The expiration date of the ban.
            If no bans are found, returns None.
    """
    banlist = json.loads(response_text)
    last_page = banlist['lastpage']
    if banlist['totalpunish'] == '0':
        return None

    bans = []
    player_name: str = url.split("&")[1].split("=")[1]
    base_url: str = url.split('?')[0] + "?type=player&player={}&page={}&perpage=25"

    tasks = [fetch_page(session, base_url, player_name, page) for page in range(1, last_page + 1)]
    _bans_list = await asyncio.gather(*tasks)
    
    bans = [
    {
        'source': tldextract.extract(url).domain,
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


async def handle_request(url, session):
    """
    Asynchronously handles a request to a given URL using a provided session.

    Args:
        url (str): The URL to make the request to.
        session (aiohttp.ClientSession): The session to use for making the request.

    Returns:
        list: A list of bans obtained from parsing the website HTML, if the request was successful.
    """
    try:
        print(f"Fetching {url}...")
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                bans = await parse_website_html(await response.text(), session, url)
                return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
    except aiohttp.client.ClientConnectorError:
        print(traceback.format_exc() + url)
