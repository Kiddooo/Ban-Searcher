from bs4 import BeautifulSoup
import asyncio
from utils import USER_AGENT
import logging
import tldextract
import traceback
import datetime


PLAYER_DOESNT_EXIST = "Player doesn't exist"
NO_BANS = "No bans have been filed."
NO_PERM_BANS = "No permanent bans have been filed."
NO_AUTO_BANS = "No automatic bans have been filed."

async def handle_request(url, session):
    try:
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                response_text = await response.text()
                _bans = []
                bans, perm_bans, auto_bans = await asyncio.gather(
                    get_bans(response_text, 'bans', url),
                    get_bans(response_text, 'permbans', url),
                    get_bans(response_text, 'autobans', url)
                )
                for ban in (bans, perm_bans, auto_bans):
                    if ban is not None:
                        _bans.extend(ban)
                return _bans
    except Exception as e:
        logging.error(f"Error: {traceback.format_exc()}, URL: {url}")


async def get_bans(response_text, ban_type, url):
    soup = BeautifulSoup(response_text, 'html.parser')
    
    if soup.find('div', class_='alert alert-danger text-center'):
        if PLAYER_DOESNT_EXIST in soup.find('div', class_='alert alert-danger text-center').text:
            return []

    bans = []
    ban_element = soup.find_all('div', class_='tab-pane', id=ban_type)

    if not ban_type in ban_element[0].text:
        table = ban_element[0].find('table', class_='table table-striped table-condensed')
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')
                ban = {
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': columns[0].text,
                    'date': int(datetime.datetime.strptime(columns[1].text, "%Y-%m-%d %H:%M:%S").timestamp()),
                    'expires': 'N/A' if columns[2].text == "" else int(datetime.datetime.strptime(columns[2].text, "%Y-%m-%d %H:%M:%S").timestamp()),
                }
                bans.append(ban)
        return bans
    return None
