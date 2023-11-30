import requests
import logging
from bs4 import BeautifulSoup
import urllib.parse
import traceback
import re
import tldextract
import json
import datetime
from WebsiteBaseHandler import BaseHandler

DATE_FORMAT_LITEBANS = "%B %d, %Y, %H:%M"

pattern = re.compile(
  r"(\bNon è mai entrato\b)|(\bNo ha entrado al servidor\b)|(\bnot found in database\b)|(\bhas not joined before\b)|(\bEventyrCraftIngen Straffe Fundet\b)|(\bNo se encontraron sanciones.\b)",
  re.IGNORECASE)

class LiteBansHandler(BaseHandler):
    def handle_request(self, url):
        try:
            if 'saicopvp' in url:
                response_text = self.get_flaresolverr_response(url)
                if response_text is not None:
                    bans = self.parse_saico_website_html(response_text, url)
                    return bans
            else:
                response_text = self.get_response(url)
                if response_text is not None:
                    bans = self.parse_website_html(response_text, url)
                    return bans
        except requests.exceptions.RequestException:
            logging.error(f"Exception occurred: {traceback.format_exc()}, URL: {url}")

    def generate_ban(self, columns, url):
        ban_expiry = columns[5].text.split("(")[0].strip()

        if ban_expiry in ("Permanent Ban", "Permanentni", "Ban Permanente"):
            ban_expires = "Permanent"
        else:
            try:
                ban_expires = int(datetime.datetime.strptime(ban_expiry, DATE_FORMAT_LITEBANS).timestamp())
            except ValueError:
                ban_expiry = ban_expiry.replace("klo", "")
                ban_expires = int(datetime.datetime.strptime(ban_expiry, '%d.%m.%Y %H:%M').timestamp())

        try:
            ban_date = int(datetime.datetime.strptime(columns[4].text, DATE_FORMAT_LITEBANS).timestamp())
        except ValueError:
            ban_date = int(datetime.datetime.strptime(columns[4].text.replace("klo", ""), '%d.%m.%Y %H:%M').timestamp())

        ban = {
            'source': tldextract.extract(url).domain,
            'url': url,
            'reason': columns[3].text,
            'date': ban_date,
            'expires': ban_expires
        }
        return ban

    def parse_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')
        bans = []
        if soup.find_all(string="No punishments found."):
            return bans

        if pattern.search(soup.text):
            return bans

        while True:
            try:
                table = soup.find('table')
                for row in table.find_all('tr')[1:]: # Skip the header row
                    columns = row.find_all('td')
                    for col in columns:
                        span = col.find('span', class_='badge litebans-label-history litebans-label-ban')
                        if span:
                            ban = self.generate_ban(columns, url)
                            bans.append(ban)
                        if span is None:
                            span = col.find('span', class_='label label-ban')
                            if span:
                                ban = self.generate_ban(columns, url)
                                bans.append(ban)


                next_page = soup.find("a", class_="litebans-pager litebans-pager-right litebans-pager-active")
                if next_page is None:
                    next_page = soup.find('div', class_='litebans-pager litebans-pager-right litebans-pager-active')
                    if next_page:
                        next_page = next_page.parent
                    if next_page is None:
                        break
                response = requests.get(urllib.parse.urljoin(url, next_page['href']), timeout=60)
                soup = BeautifulSoup(response.text(), 'html.parser')
            except AttributeError:
                # logging.error(f"AttributeError occurred: {url}", traceback.format_exc())
                break

        return bans

    def parse_saico_website_html(self, response_text, url):
        soup = BeautifulSoup(response_text, 'html.parser')
        bans = []

        if soup.find_all(string="No punishments found."):
            return bans

        if pattern.search(soup.text):
            return bans

        while True:
            try:
                table = soup.find('table')
                for row in table.find_all('tr')[1:]: # Skip the header row
                    columns = row.find_all('td')
                    for col in columns:
                        span = col.find('span', class_='label label-ban')
                        if span:
                            ban = {
                                'source': tldextract.extract(url).domain,
                                'url': url,
                                'reason': columns[3].text,
                                'date': int(datetime.datetime.strptime(columns[4].text.replace("AM", "").replace("PM", "").strip(), DATE_FORMAT_LITEBANS).timestamp()),
                                'expires': "Permanent" if "Permanent Ban" in columns[5].text else int(datetime.datetime.strptime(columns[4].text.replace("AM", "").replace("PM", "").strip(), DATE_FORMAT_LITEBANS).timestamp())
                            }
                            bans.append(ban)

                next_page = soup.find('div', class_="litebans-pager litebans-pager-right litebans-pager-active")
                if next_page is None:
                    break
                else:
                    headers = {'Content-Type': 'application/json'}
                    data = {
                        "cmd": "request.get",
                        "url": f"{urllib.parse.urljoin(url, next_page.parent['href'])}",
                        "maxTimeout": 60000
                    }
                    with requests.post(self.FLARESOLVER_URL, data=json.dumps(data), headers=headers, timeout=60) as response:
                        response_html = response.json()
                        soup = BeautifulSoup(response_html.get('solution').get('response'), 'html.parser')
            except AttributeError:
                logging.error(f"AttributeError occurred: {traceback.format_exc()}")
                break

        return bans
