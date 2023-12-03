import json
from WebsiteBaseHandler import BaseHandler
import tldextract
from datetime import datetime

from utils import get_language, translate

class MCCentralHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        bans = []
        json_response = json.loads(response_text)['results']

        if json_response['offence_count'] != 0:
            for offence in json_response['offences']:
                if offence['timeleft'] != 'Appealed':
                    ban_reason = offence['reason']
                    bans.append({
                        'source': tldextract.extract(url).domain,
                        'url': url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': int(datetime.strptime(offence['datetime'].replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").replace("Augu", "August"), "%d %B %Y").timestamp()),
                        'expires': "Permanent" if offence['timeleft'] == "Forever" else "N/A"
                    })
        return bans
