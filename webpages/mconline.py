import requests
import tldextract
from tqdm import tqdm


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
def parse_website_html(response_text, url):
    try:
        bans = []
        _ban = response_text.split("\n")[3:-1][0].split(';')
        ban = {
            'source': tldextract.extract(url).domain,
            'url': url,
            'date': _ban[1],
            'reason': _ban[2],
            'expires': 'N/A'
        }
        bans.append(ban)
    except IndexError:
        pass
    
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