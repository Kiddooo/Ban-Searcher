import aiohttp
import traceback
import tldextract

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
async def parse_website_html(response_text, url):
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

async def handle_request(url, session):
    try:
        print(f"Fetching {url}...")
        async with session.get(url,headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                bans = await parse_website_html(await response.text(), url)
                return bans
    except AttributeError as e:
        print(traceback.format_exc() + url)
    except aiohttp.client.ClientConnectorError as e:
        print(traceback.format_exc() + url)