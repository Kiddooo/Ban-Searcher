import requests
from bs4 import BeautifulSoup, Comment
from utils import USER_AGENT
import tldextract
import datetime
from tqdm import tqdm
import traceback

DATE_FORMAT = "%b %d, %Y %I:%M:%S %p"

def parse_website_html(response_text, url):
    soup = BeautifulSoup(response_text, 'html.parser')

    if soup.find('strong', text='Unknown User'):
        return None

    bans = []
    
    if soup.find(text=lambda text: isinstance(text, Comment) and 'user.ban_received_table_start' in text):
        table = soup.find_all('table', class_='table table-bordered')[0]
        if table is not None:
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')
                ban = {
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': columns[2].text,
                    'date': "N/A",
                    'expires': "Permanent" if "Permanent" in columns[3].text else int(datetime.datetime.strptime(columns[3].text, DATE_FORMAT).timestamp())
                }
                bans.append(ban)
        return bans


def handle_request(url):
    try:
        tqdm.write(f"Fetching {url}...")
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        if response.status_code == 200:
            bans = parse_website_html(response.text, url)
            return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
