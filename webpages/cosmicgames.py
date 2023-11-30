import json
from WebsiteBaseHandler import BaseHandler
import tldextract

class CosmicGamesHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        json_response = json.loads(response_text)
        bans = []
        if len(json_response) != 0:
            for offence in json_response:
                if offence['type'].lower() == 'ban'.lower():
                    bans.append({
                        'source': tldextract.extract(url).domain,
                        'url': url,
                        'reason': offence['reason'],
                        'date': int(offence['time'] / 1000),
                        'expires': int(offence['expiration'] / 1000)
                    })
        return bans