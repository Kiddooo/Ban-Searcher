import json
from WebsiteBaseHandler import BaseHandler
import tldextract

from utils import get_language, translate

class CosmicGamesHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        json_response = json.loads(response_text)
        bans = []
        if len(json_response) != 0:
            for offence in json_response:
                if offence['type'].lower() == 'ban'.lower():
                    ban_reason = offence['reason']
                    bans.append({
                        'source': tldextract.extract(url).domain,
                        'url': url,
                        'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                        'date': int(offence['time'] / 1000),
                        'expires': int(offence['expiration'] / 1000)
                    })
        return bans