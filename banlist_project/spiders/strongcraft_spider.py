import dateparser
import scrapy
from bs4 import BeautifulSoup
import tldextract
from datetime import date, timedelta, datetime
import re
from banlist_project.items import BanItem
from utils import get_language, translate

class StrongcraftSpider(scrapy.Spider):
    name = 'StrongcraftSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(StrongcraftSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        url = "https://www.strongcraft.org/players/" + self.player_username
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        if soup.find(text='Here you can look for the profile of any player on our network.'):
            return

        ban_indicator = soup.find('div', class_='user-data').find_all('div')
        if len(ban_indicator) == 2:
            return
        else:
            if len(ban_indicator) == 3:
                if 'banned' not in ban_indicator[2].text.lower().strip():
                    return
                else:
                    table = soup.find_all('div', class_='container youplay-content')[0]
                    if table is not None:
                        row = table.find_all('p')[1:][1] # Skip the header row

                        website_ban_date = row.text.split("(")[0].replace("The player is banned since ", "")

                        ban_reason = row.text.split("(")[1].split(")")[0]
                        yield BanItem({
                            'source': tldextract.extract(response.url).domain,
                            'url': response.url,
                            'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                            'date': int(dateparser.parse(website_ban_date).timestamp()),
                            'expires':"Permanent" if row.text.split(",")[1].strip() == "ban is permanent." else row.text.split(",")[1].strip()
                        })