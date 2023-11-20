import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import traceback
from utils import USER_AGENT

async def parse_website_html(response_text, session, url):
    if response_text == "":
        return []
    
    soup = BeautifulSoup(response_text, 'html.parser')

    bans = []

    while True:
        table = soup.find_all('table', class_='i-table fullwidth')[1]
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')[1:-1]
                ban = {
                    'banID': columns[0].text,
                    'server': columns[1].text,
                    'bannedBy': columns[2].text,
                    'Reason': columns[3].text,
                    'TimeBanned': columns[4].text
                }
                bans.append(ban)

        pagination_link = soup.find('span', class_='fa fa-step-forward')
        if 'disabled' in pagination_link.parent.get('class'):
            # No more pages
            break
        else:
            next_page_url = urljoin(url, pagination_link.parent['href'])
            async with session.get(next_page_url) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')


    return bans


async def handle_request(url, session):
    try:
        print(url)
        async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                bans = await parse_website_html(await response.text(), session, url)
                return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
    except aiohttp.client.ClientConnectorError:
        print(traceback.format_exc() + url)