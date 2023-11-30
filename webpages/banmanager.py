from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from WebsiteBaseHandler import BaseHandler
import tldextract
import re
import time

class BanManagerHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')

        bans = []

        # Get current ban
        current_ban_table = soup.find('table', id='current-ban')
        if current_ban_table is not None:
            if current_ban_table.find('tr').find('td').text != 'None':
                current_ban = {}
                for row in current_ban_table.find_all('tr'):
                    columns = row.find_all('td')
                    if len(columns) == 2:  # Ensure there are exactly 2 columns
                        current_ban[columns[0].text.replace(':', '').lower()] = columns[1].text

                # Format the current ban information
                current_ban = list(current_ban.items())
                bans.append({
                    'source': tldextract.extract(url).domain,
                    'url': url,
                    'reason': current_ban[3][1],
                    'date': int(datetime.strptime(current_ban[2][1], "%d %B %Y %I:%M:%S %p").timestamp()),
                    'expires': int(self.parse_expiry_date(current_ban[0][1]))
                })
        
        # Get previous bans
        previous_bans_table = soup.find('table', id='previous-bans')
        if previous_bans_table is not None:
            if previous_bans_table.find_all('tr')[1:][0].find('td').text != 'None':
                for row in previous_bans_table.find_all('tr')[1:]:  # Skip the header row
                    columns = row.find_all('td')
                    if len(columns) >= 7:  # Ensure there are at least 7 columns
                        bans.append({
                            'source': tldextract.extract(url).domain,
                            'url': url,
                            'reason': columns[1].text,
                            'date': int(datetime.strptime(columns[3].text, '%H:%M:%S %d/%m/%y').timestamp()),
                            'expires': int(datetime.strptime(columns[6].text, '%H:%M:%S %d/%m/%y').timestamp())
                        })
        return bans
    
    def parse_expiry_date(self, ban_date):
        duration_units = {
            'year': 'years',
            'month': 'months',
            'week': 'weeks',
            'day': 'days',
            'hour': 'hours',
            'minute': 'minutes',
            'second': 'seconds'
        }

        # Split the duration string into parts
        parts = ban_date.split(',')

        # Initialize the duration dictionary
        duration_dict = {}

        # For each part, extract the number and the time unit, and add to the duration dictionary
        for part in parts:
            # Extract the number and the time unit
            match = re.match(r'(\d+)\s+(\w+)', part.strip())
            if match:
                number = int(match.group(1))
                unit = match.group(2)
                if unit.endswith('s'):
                    unit = unit[:-1]  # Remove the 's' at the end
                # Add to the duration dictionary
                duration_dict[duration_units[unit]] = number

        # Create a relativedelta object from the duration dictionary
        duration = relativedelta(**duration_dict)

        # Get the current datetime
        now = datetime.now()

        # Calculate the future datetime
        future_datetime = now + duration

        # Convert the future datetime to a Unix timestamp
        future_timestamp = time.mktime(future_datetime.timetuple())
        
        return future_timestamp