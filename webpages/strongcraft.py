from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract
from datetime import date, timedelta, datetime
import re

from utils import get_language, translate

class StrongcraftHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')

        if soup.find(text='Here you can look for the profile of any player on our network.'):
            return None

        bans = []
        ban_indicator = soup.find('div', class_='user-data').find_all('div')
        if len(ban_indicator) == 2:
            return None
        else:
            if len(ban_indicator) == 3:
                if 'banned' not in ban_indicator[2].text.lower().strip():
                    return None
                else:
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
                        ban_reason = row.text.split("(")[1].split(")")[0]
                        ban = {
                            'source': tldextract.extract(url).domain,
                            'url': url,
                            'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                            'date': int(date_object.timestamp()),
                            'expires':"Permanent" if row.text.split(",")[1].strip() == "ban is permanent." else row.text.split(",")[1].strip()

                        }
                        bans.append(ban)
        return bans