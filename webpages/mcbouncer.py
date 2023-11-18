from bs4 import BeautifulSoup
from urllib.parse import urljoin
import traceback
import aiohttp
from utils import USER_AGENT

previous_next_page_url = None


async def parse_website_html(response_text, session, url: str):
    soup = BeautifulSoup(response_text, 'html.parser')

    bans = []

    while True:
        table = soup.find('table')
        if table is not None:
            for row in table.find_all('tr')[1:]:  # Skip the header row
                columns = row.find_all('td')
                ban = {
                    'bannedBy': columns[0].text,
                    'Reason': columns[1].text,
                    'TimeBanned': columns[2].text.replace('\xa0', " "),
                    'Server': columns[3].text
                }
                bans.append(ban)

        # Find the "Next" button and its parent li element
        next_button = soup.find('a', string='»')
        if next_button is not None:
            next_button_parent = next_button.find_parent('li')

            # If the parent li element has the "disabled" class, it means that there are no more pages
            if 'disabled' in next_button_parent.get('class', []):
                break

            # Join the base URL with the href of the next page to get the full URL of the next page
            next_page_url = urljoin(url, next_button['href'])

            # Send a GET request to the next page
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
    except aiohttp.client.ClientConnectorError as e:
        print(traceback.format_exc() + url)
