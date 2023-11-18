import logging
from bs4 import BeautifulSoup, FeatureNotFound
import aiohttp
import urllib.parse
import traceback
import re
import tldextract
from tqdm import tqdm
import json
from utils import FLARESOLVER_URL, USER_AGENT

pattern = re.compile(
  r"(\bNon è mai entrato\b)|(\bNo ha entrado al servidor\b)|(\bnot found in database\b)|(\bhas not joined before\b)",
  re.IGNORECASE)


# Define a helper function
def extract_ban_info(row, url):
   """Extract ban information from a row in the table."""
   columns = row.find_all('td')
   for col in columns:
       span = col.find('span', class_='badge litebans-label-history litebans-label-ban')
       if span:
           return {
               'source': tldextract.extract(url).domain,
               'url': url,
               'reason': columns[3].text,
               'date': columns[4].text,
               'expires': columns[5].text
           }
   return None

async def parse_website_html(session, response_text, url):
    """Parse the HTML of a website and extract ban information."""
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
                        ban = {
                            'source': tldextract.extract(url).domain,
                            'url': url,
                            'reason': columns[3].text,
                            'date': columns[4].text,
                            'expires': columns[5].text
                        }
                        bans.append(ban)

            next_page = soup.find("a", class_="litebans-pager litebans-pager-right litebans-pager-active")
            if next_page is None:
                break
            response = await session.get(urllib.parse.urljoin(url, next_page['href']))
            soup = BeautifulSoup(await response.text(), 'html.parser')
        except AttributeError:
            logging.error(f"AttributeError occurred: {url}")
            break

    return bans

async def handle_request(url, session):
   """Handle a request to a website and extract ban information."""
   logging.info(url)
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
    """Extract ban information from the HTML of a Saico website."""
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
                            'date': columns[4].text,
                            'expires': columns[5].text
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
   """Handle a request to a Saico website and extract ban information."""
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