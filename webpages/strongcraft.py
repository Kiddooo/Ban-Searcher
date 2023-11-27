# https://www.strongcraft.org/players/martusin/

import aiohttp
from bs4 import BeautifulSoup
import traceback
from utils import USER_AGENT
import tldextract
from datetime import date, timedelta, datetime
import re

async def parse_website_html(response_text, url):
    """
    Parse the HTML response text of a website and extract information about banned players.

    Parameters:
        response_text (str): The HTML response text of the website.

    Returns:
        list: A list of dictionaries containing information about banned players. Each dictionary has the following keys:
            - reason (str): The reason for the ban.
            - Expires (str): The expiration date of the ban.
            - timeBanned (str): The duration of time the player has been banned.

        None: If the HTML response text does not contain information about banned players.
    """
    soup = BeautifulSoup(response_text, 'html.parser')

    if soup.find(text='Here you can look for the profile of any player on our network.'):
        return None

    bans = []
    ban_indicator = soup.find('div', class_='user-data').find_all('div')[2].text
    if not 'Banned' in ban_indicator:
        return None
    
    table = soup.find_all('div', class_='container youplay-content')[0]
    if table is not None:
        row = table.find_all('p')[1:][1] # Skip the header row

        website_ban_date = row.text.split("(")[0].replace("The player is banned since ", "").replace("ago", "").strip()

        matches = re.findall(r"(\d+)\s*(months|weeks|days|minutes|seconds)", website_ban_date)

        time_duration = timedelta(
            weeks=int(next((x for x in matches if x[1] == "weeks"), (0, "weeks"))[0]),
            days=int(next((x for x in matches if x[1] == "days"), (0, "days"))[0]),
            minutes=int(next((x for x in matches if x[1] == "minutes"), (0, "minutes"))[0]),
            seconds=int(next((x for x in matches if x[1] == "seconds"), (0, "seconds"))[0])
        )

        date_object = datetime.combine(date.today() - time_duration, datetime.min.time())

        ban = {
            'source': tldextract.extract(url).domain,
            'url': url,
            'reason': row.text.split("(")[1].split(")")[0],
            'date': int(date_object.timestamp()),
            'expires':"Permanent" if row.text.split(",")[1].strip() == "ban is permanent." else row.text.split(",")[1].strip()
            
        }
        bans.append(ban)
    return bans


async def handle_request(url, session):
    """
    Asynchronously handles a request to a specified URL using the provided session object.

    Args:
        url (str): The URL to send the request to.
        session (aiohttp.ClientSession): The session object to use for the request.

    Returns:
        list: A list of bans extracted from the website HTML response, if the response status is 200.

    Raises:
        AttributeError: If an AttributeError occurs during the request.
        aiohttp.client.ClientConnectorError: If a ClientConnectorError occurs during the request.
    """
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
