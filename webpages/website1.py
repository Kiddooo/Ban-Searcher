# Litebans

from bs4 import BeautifulSoup
import requests
import urllib.parse
import traceback
import re
import tldextract
from tqdm import tqdm

pattern = re.compile(
    r"(\bNon è mai entrato\b)|(\bNo ha entrado al servidor\b)|(\bnot found in database\b)|(\bhas not joined before\b)",
    re.IGNORECASE)


def parse_website_html(reponse_text: str, url: str):
    soup = BeautifulSoup(reponse_text, 'html.parser')

    bans = []

    if soup.find_all(string="No punishments found."):
        return bans

    if pattern.search(soup.text):
        return bans

    while True:
        table = soup.find('table')
        for row in table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            for col in columns:
                span = col.find(
                    'span',
                    class_='badge litebans-label-history litebans-label-ban')
                if span:
                    ban = {
                        'source': tldextract.extract(url).domain,
                        'url': url,
                        'reason': columns[3].text,
                        'date': columns[4].text,
                        'expires': columns[5].text
                    }
                    bans.append(ban)

        next_page = soup.find(
            "a",
            class_="litebans-pager litebans-pager-right litebans-pager-active")
        if next_page is None:
            break
        response = requests.get(urllib.parse.urljoin(url, next_page['href']))
        soup = BeautifulSoup(response.text, 'html.parser')

    
    return bans



def handle_request(url: str):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            },
            cookies={"_cosmic_auth": "f8c9391e30d6ea3d8c849ec2a36fd7d8"})

        if response.status_code == 200:
            bans = parse_website_html(response.text, url)

            return bans
    except requests.exceptions.ReadTimeout:
        pass
    except AttributeError as e:
        print(traceback.format_exc() + url)
        pass
