import json
import utils
from webpages import litebans, mcbouncer, mcbans, mconline, johnmuffin, mccentral, cosmicgames
from aiohttp import ClientSession
import asyncio

PLAYER_USERNAME = input("Enter a username: ")
PLAYER_UUID = utils.UsernameToUUID(PLAYER_USERNAME)
PLAYER_UUID_DASH = utils.UUIDToUUIDDash(PLAYER_UUID)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

def get_headers():
    headers = {"User-Agent": USER_AGENT}
    return headers

with open("websites.json", "r") as external_json_urls:
   external_urls = json.load(external_json_urls)


async def main():
    async with ClientSession(headers=get_headers()) as session:
        for url_type in external_urls:
            # if url_type == "LITEBANS":
            #     LiteBansBans = await asyncio.gather(*[litebans.handle_request(url.replace("<UUID>", PLAYER_UUID).replace("<UUID-DASH>", PLAYER_UUID_DASH), session) for url in external_urls[url_type]])
            #     print(f"LiteBans: {[ban for ban in LiteBansBans if ban is not None and len(ban) > 0]}\n")
            
            # if url_type == 'MCBOUNCER':
            #     MCBouncerBans = await asyncio.gather(*[mcbouncer.handle_request(url.replace("<UUID>", PLAYER_UUID), session) for url in external_urls[url_type]])
            #     print(f"MCBouncer: {[ban for ban in MCBouncerBans if ban is not None and len(ban) > 0]}\n")
            
            # if url_type == 'MCBANS':
            #     MCBansBans = await asyncio.gather(*[mcbans.handle_request(url.replace("<UUID>", PLAYER_UUID), session) for url in external_urls[url_type]])
            #     print(f"MCBans: {[ban for ban in MCBansBans[0][:-1] if ban is not None and len(ban) > 0]}\n")
            
            # if url_type == 'MCONLINE':
            #     MCOnlineBans = await asyncio.gather(*[mconline.handle_request(url.replace("<USERNAME>", PLAYER_USERNAME), session) for url in external_urls[url_type]])
            #     print(f"MCOnline: {[ban for ban in MCOnlineBans if ban is not None and len(ban) > 0]}\n")
            
            # if url_type == 'JOHNYMUFFIN':
            #     JohnyMuffinBans = await asyncio.gather(*[johnmuffin.handle_request(url.replace("<UUID-DASH>", PLAYER_UUID_DASH), session) for url in external_urls[url_type]])
            #     print(f"JohnnyMuffin: {[ban for ban in JohnyMuffinBans if ban is not None and len(ban) > 0]}\n")
            
            # if url_type == 'MCCENTRAL':
            #     MCCentralBans = await asyncio.gather(*[mccentral.handle_request(url.replace("<UUID>", PLAYER_UUID), session) for url in external_urls[url_type]])
            #     print(f"MCCentral: {[ban for ban in MCCentralBans if ban is not None and len(ban) > 0]}\n")
            
            if url_type == 'MCBRAWL':
                print(f"MCBrawl: {external_urls[url_type]}\n")
            
            if url_type == 'COSMICPRISON':
                CosmicPrisonBans = await asyncio.gather(*[cosmicgames.handle_request(url.replace("<USERNAME>", PLAYER_USERNAME), session) for url in external_urls[url_type]])
                print(f"CosmicPrison: {[ban for ban in CosmicPrisonBans if ban is not None and len(ban) > 0]}\n")
                # print(f"CosmicPrison: {external_urls[url_type]}\n")
            
            if url_type == 'STRONGCRAFT':
                print(f"StrongCraft: {external_urls[url_type]}\n")
            
            if url_type == 'MANACUBE':
                print(f"ManaCube: {external_urls[url_type]}\n")

if __name__ == "__main__":
	asyncio.run(main())