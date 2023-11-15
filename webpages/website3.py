# Mcbouner
# https://mcbouncer.com/u/ad37bc56401c47b299c61080f2603c50/

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import traceback
import re

previous_next_page_url = None


def parse_website_html(reponse_text: str, url: str):
    soup = BeautifulSoup(reponse_text, 'html.parser')

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
            response = requests.get(next_page_url)
            soup = BeautifulSoup(response.text, 'html.parser')

    return bans


def handle_request(url: str, username):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bans = parse_website_html(response.text, url)
            if (len(bans) >= 1):
                print(f"Found {len(bans)} bans for {username} at {url}")
    except AttributeError as e:
        print(traceback.format_exc() + url)
