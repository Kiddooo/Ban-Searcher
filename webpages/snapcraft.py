# https://snapcraft.net/bans/search/TheLionTR/

import aiohttp
from bs4 import BeautifulSoup
import traceback
from utils import USER_AGENT
import tldextract
from datetime import datetime

async def parse_website_html(response_text, url):
    """
    Parse the HTML of a website response and extract ban information.

    Args:
        response_text (str): The HTML content of the website response.

    Returns:
        list: A list of dictionaries containing ban information. Each dictionary
            has the following keys:
            - 'reason': The reason for the ban.
            - 'bannedBy': The staff member who issued the ban.
            - 'banDate': The date the ban was issued.
            - 'banExpiry': The date the ban will expire.
    """
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


async def handle_request(url, session):
    """
    Asynchronously handles a request by sending a GET request to the specified URL using the provided session object.
    
    Parameters:
    - url (str): The URL to send the GET request to.
    - session (aiohttp.ClientSession): The session object to use for sending the request.
    
    Returns:
    - bans (List[str]): A list of ban URLs parsed from the website HTML, or None if the response status is not 200.
    """
    try:
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                bans = await parse_website_html(await response.text(), url)
                return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
    except aiohttp.client.ClientConnectorError:
        print(traceback.format_exc() + url)
