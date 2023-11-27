import aiohttp
from bs4 import BeautifulSoup
import traceback
from utils import USER_AGENT
import tldextract
import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

async def parse_website_html(response_text, url):
    
    username = url.split("?username=")[1].strip()
    
    soup = BeautifulSoup(response_text, "html.parser")

    bans = []
    
    table = soup.find_all("table")
    for row in table[0].find_all('tr')[1:]:
        columns = row.find_all('td')
        if columns[0].text == username:   
            time_units = {
                "hours": "hours",
                "days": "days",
                "minutes": "minutes",
                "permanent": "permanent"
            }

            for unit in time_units:
                if unit in columns[3].text:
                    if unit == "permanent":
                        ban_expires = "Permanent"
                    else:
                        expire_amount = int(columns[3].text.replace(unit, "").strip())
                        ban_expires = datetime.datetime.strptime(columns[1].text, DATE_FORMAT) + datetime.timedelta(**{time_units[unit]: expire_amount})
                    
            ban = {
                'source': tldextract.extract(url).domain,
                'url': url,
                'reason': columns[2].text,
                'date': int(datetime.datetime.strptime(columns[1].text, DATE_FORMAT).timestamp()),
                'expires': ban_expires if type(ban_expires) == str else int(ban_expires.timestamp())
            }
            
            bans.append(ban)
    return bans


async def handle_request(url, session):
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
