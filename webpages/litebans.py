import logging
from bs4 import BeautifulSoup
import aiohttp
import urllib.parse
import traceback
import re
import tldextract
import json
from utils import FLARESOLVER_URL, USER_AGENT
import datetime

pattern = re.compile(
  r"(\bNon è mai entrato\b)|(\bNo ha entrado al servidor\b)|(\bnot found in database\b)|(\bhas not joined before\b)|(\bEventyrCraftIngen Straffe Fundet\b)",
  re.IGNORECASE)

DATE_FORMAT_LITEBANS = "%B %d, %Y, %H:%M"

def generate_ban(columns, url):
    ban_expiry = columns[5].text.split("(")[0].strip()

    if ban_expiry in ("Permanent Ban", "Permanentni", "Ban Permanente"):
        ban_expires = "Permanent"
    else:
        ban_expires = int(datetime.datetime.strptime(ban_expiry, DATE_FORMAT_LITEBANS).timestamp())
    ban = {
        'source': tldextract.extract(url).domain,
        'url': url,
        'reason': columns[3].text,
        'date': int(datetime.datetime.strptime(columns[4].text, DATE_FORMAT_LITEBANS).timestamp()),
        'expires': ban_expires
    }
    return ban

async def parse_website_html(session, response_text, url):
    """
    Parses the HTML of a website to extract ban information.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session to make HTTP requests.
        response_text (str): The HTML response text of the website.
        url (str): The URL of the website.

    Returns:
        list: A list of dictionaries containing ban information. Each dictionary has the following keys:
            - 'source' (str): The domain of the website.
            - 'url' (str): The URL of the website.
            - 'reason' (str): The reason for the ban.
            - 'date' (str): The date of the ban.
            - 'expires' (str): The expiration date of the ban.
    """
    soup = BeautifulSoup(response_text, 'html.parser')
    bans = []
    if soup.find_all(string="No punishments found."):
       return bans

    if pattern.search(soup.text):
       return bans

    while True:
        try:
            table = soup.find('table')
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')
                for col in columns:
                    span = col.find('span', class_='badge litebans-label-history litebans-label-ban')
                    if span:
                        ban = generate_ban(columns, url)
                        bans.append(ban)
                    if span is None:
                        span = col.find('span', class_='label label-ban')
                        if span:
                            ban = generate_ban(columns, url)
                            bans.append(ban)


            next_page = soup.find("a", class_="litebans-pager litebans-pager-right litebans-pager-active")
            if next_page is None:
                next_page = soup.find('div', class_='litebans-pager litebans-pager-right litebans-pager-active')
                if next_page:
                    next_page = next_page.parent
                if next_page is None:
                    break
            response = await session.get(urllib.parse.urljoin(url, next_page['href']))
            soup = BeautifulSoup(await response.text(), 'html.parser')
        except AttributeError:
            logging.error(f"AttributeError occurred: {url}", traceback.format_exc())
            break

    return bans

async def handle_request(url, session):
   """
   Asynchronously handles a request by sending a GET request to the specified URL using the given session.

   Args:
       url (str): The URL to send the GET request to.
       session (aiohttp.ClientSession): The session to use for sending the request.

   Returns:
       list: A list of bans, if the request is successful and the URL matches "saicopvp" or if the response status is 200 and the website HTML is successfully parsed.
   """
   try:
       if "saicopvp" in url:
           bans = await handle_request_saico(url, session)
           return bans
       else:
           async with session.get(url,headers={"User-Agent": USER_AGENT}) as response:
               if response.status == 200:
                  bans = await parse_website_html(session, await response.text(), url)
                  return bans
   except aiohttp.ServerTimeoutError:
       pass
   except aiohttp.ClientConnectionError:
       pass
   except Exception as e:
       logging.error(f"Exception occurred: {traceback.format_exc()}")


async def parse_saico_website_html(session, response_text, url):
    """
    Parses the HTML response from the Saico website to extract ban information.

    Args:
        session (aiohttp.ClientSession): The HTTP session to use for making requests.
        response_text (str): The HTML response text.
        url (str): The URL of the Saico website.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the extracted ban information. Each dictionary contains the following keys:
            - source (str): The domain of the Saico website.
            - url (str): The URL of the ban.
            - reason (str): The reason for the ban.
            - date (str): The date the ban was issued.
            - expires (str): The expiration date of the ban. Empty string if the ban does not expire.
    """
    soup = BeautifulSoup(response_text, 'html.parser')
    bans = []

    if soup.find_all(string="No punishments found."):
        return bans

    if pattern.search(soup.text):
        return bans

    while True:  
        try:
            table = soup.find('table')
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')
                for col in columns:
                    span = col.find('span', class_='label label-ban')
                    if span:
                        ban = {
                            'source': tldextract.extract(url).domain,
                            'url': url,
                            'reason': columns[3].text,
                            'date': int(datetime.datetime.strptime(columns[4].text.replace("AM", "").replace("PM", "").strip(), DATE_FORMAT_LITEBANS).timestamp()),
                            'expires': "Permanent" if "Permanent Ban" in columns[5].text else int(datetime.datetime.strptime(columns[4].text.replace("AM", "").replace("PM", "").strip(), DATE_FORMAT_LITEBANS).timestamp())
                        }
                        bans.append(ban)

            next_page = soup.find('div', class_="litebans-pager litebans-pager-right litebans-pager-active")
            if next_page is None:
                break
            else:
                headers = {'Content-Type': 'application/json'}
                data = {
                    "cmd": "request.get",
                    "url": f"{urllib.parse.urljoin(url, next_page.parent['href'])}",
                    "maxTimeout": 60000
                }
                async with session.post(FLARESOLVER_URL, data=json.dumps(data), headers=headers) as response:
                    response_html = await response.json()
                    soup = BeautifulSoup(response_html.get('solution').get('response'), 'html.parser')
        except AttributeError:
            logging.error(f"AttributeError occurred: {traceback.format_exc()}")
            break

    return bans

async def handle_request_saico(url, session):
   """
   Asynchronously handles a request to the Saico API.

   Args:
       url (str): The URL to send the request to.
       session (aiohttp.ClientSession): The aiohttp client session to use for making the request.

   Returns:
       list: A list of bans parsed from the Saico website.

   Raises:
       None
   """
   headers = {'Content-Type': 'application/json'}
   data = {
       "cmd": "request.get",
       "url": f"{url}",
       "maxTimeout": 60000
   }
   async with session.post(FLARESOLVER_URL, data=json.dumps(data), headers=headers) as response:
       response_html = await response.json()
       if response_html.get('solution').get('status') == 200:
           bans = await parse_saico_website_html(session, response_html.get('solution').get('response'), url)
           return bans
       else: 
           logging.error(f"AttributeError occurred: fuckin saico")