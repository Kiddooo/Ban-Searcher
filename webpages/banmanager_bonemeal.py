from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re


class BanManagerBonemealHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')

        bans = []

        # Find all timeline items
        timeline_items = soup.find_all('li', class_='timeline')

        # Find all inverted timeline items (for the second "pvp bypass" ban)
        timeline_inverted_items = soup.find_all('li', class_='timeline-inverted')

        # Combine both lists
        all_items = timeline_items + timeline_inverted_items

        for item in all_items:
            ban = {}

            # Get ban details
            ban_reason = item.find('div', class_='timeline-body').get_text().split("\n")[1].strip().split(":")[1].strip()
            
            # Get ban date
            ban_date_str = soup.find('small', class_='text-muted')['title']
            ban_date = datetime.strptime(ban_date_str, "%Y-%m-%d %H:%M:%S")
            
            # Convert the ban date to a Unix timestamp
            ban_start_timestamp = int(ban_date.timestamp())

            # Get ban length
            ban_length_str = item.find('div', class_='timeline-body').find('p')
            
            unit = None
            ban_end_date = None
            
            if ban_length_str is not None:
                ban_length_str = ban_length_str.get_text(strip=True)
                match = re.match(r'Lasted for (\d+) (\w+).', ban_length_str)
                if match:
                    number = int(match.group(1))
                    unit = match.group(2)

                    # Add the ban length to the ban start date
                    if unit == 'days':
                        ban_end_date = ban_date + relativedelta(days=number)
                    elif unit == 'weeks':
                        ban_end_date = ban_date + relativedelta(weeks=number)
                    elif unit == 'months':
                        ban_end_date = ban_date + relativedelta(months=number)
                    elif unit == 'years':
                        ban_end_date = ban_date + relativedelta(years=number)
                    # Add more conditions here if there are other possible units

                    # Convert the ban end date to a Unix timestamp
                    ban_end_timestamp = int(ban_end_date.timestamp())
                else:
                    # If ban length is not specified, skip the ban length calculation
                    ban_end_timestamp = 'N/A'
            else:
                ban_end_timestamp = 'N/A'
            
            ban['reason'] = ban_reason
            ban['timestamp'] = ban_start_timestamp
            ban['expire'] = ban_end_timestamp

            bans.append(ban)

        return bans