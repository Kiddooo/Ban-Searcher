# https://www.strongcraft.org/players/martusin/

# import aiohttp
# from bs4 import BeautifulSoup, Comment
# import traceback
# from utils import USER_AGENT

# async def parse_website_html(response_text):
#     soup = BeautifulSoup(response_text, 'html.parser')

#     if soup.find('strong', text='Unknown User'):
#         return None

#     bans = []
    
#     if soup.find(text=lambda text: isinstance(text, Comment) and 'user.ban_received_table_start' in text):
#         table = soup.find_all('table', class_='table table-bordered')[0]
#         if table is not None:
#             for row in table.find_all('tr')[1:]: # Skip the header row
#                 columns = row.find_all('td')
#                 ban = {
#                     'banID': columns[0].text,
#                     'bannedBy': columns[1].text,
#                     'Reason': columns[2].text,
#                     'Expires': columns[3].text,
#                     'Server': columns[4].text,
#                     'BanActive': columns[5].text
#                 }
#                 bans.append(ban)
#         return bans


# async def handle_request(url, session):
#     try:
#         async with session.get(url, headers={"User-Agent": USER_AGENT}) as response:
#             if response.status == 200:
#                 bans = await parse_website_html(await response.text())
#                 return bans
#     except AttributeError as e:
#         print(traceback.format_exc() + url)
#     except aiohttp.client.ClientConnectorError:
#         print(traceback.format_exc() + url)
