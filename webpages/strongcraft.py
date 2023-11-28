from bs4 import BeautifulSoup
import requests
from utils import USER_AGENT
import tldextract
from datetime import date, timedelta, datetime
import re
from tqdm import tqdm


def parse_website_html(response_text, url):
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

def handle_request(url):
    try:
        tqdm.write(f"Fetching {url}...")
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        if response.status_code == 200:
            bans = parse_website_html(response.text, url)
            return bans
    except requests.exceptions.RequestException as e:
        print(str(e) + url)