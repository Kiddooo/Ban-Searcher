import tldextract
from WebsiteBaseHandler import BaseHandler

class MCOnlineHandler(BaseHandler):
    def parse_website_html(self, response_text, url):
        try:
            bans = []
            _ban = response_text.split("\n")[3:-1][0].split(';')
            ban = {
                'source': tldextract.extract(url).domain,
                'url': url,
                'date': int(_ban[1]),
                'reason': _ban[2],
                'expires': 'N/A'
            }
            bans.append(ban)
        except IndexError:
            pass
    
        return bans