# https://bans.manacube.com/user?user=martusin#bans

from bs4 import BeautifulSoup
import asyncio
from utils import USER_AGENT
import logging
import traceback

PLAYER_DOESNT_EXIST = "Player doesn't exist"
NO_BANS = "No bans have been filed."
NO_PERM_BANS = "No permanent bans have been filed."
NO_AUTO_BANS = "No automatic bans have been filed."

async def handle_request(url, session):
   try:
       async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
           if response.status == 200:
               print(url)
               response_text = await response.text()
               bans, perm_bans, auto_bans = await asyncio.gather(
                  get_bans(response_text, 'bans'),
                  get_bans(response_text, 'permbans'),
                  get_bans(response_text, 'autobans')
               )
               return bans, perm_bans, auto_bans
   except Exception as e:
       logging.error(f"Error: {traceback.format_exc()}, URL: {url}")


async def get_bans(response_text, ban_type):
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
                  'Reason': columns[0].text,
                  'TimeBanned': columns[1].text,
                  'Expires': columns[0].text,
                  'ResolveTime': columns[3].text,
                  'Server': columns[4].text,
               }
               bans.append(ban)
       return bans
   return []
