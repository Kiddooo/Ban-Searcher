import json
import utils
from webpages import litebans, mcbouncer, mcbans, mconline, website4
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
            if url_type == "LITEBANS":
                LiteBansBans = await asyncio.gather(*[litebans.handle_request(url.replace("<UUID>", PLAYER_UUID).replace("<UUID-DASH>", PLAYER_UUID_DASH), session) for url in external_urls[url_type]])
                bans = [ban for ban in LiteBansBans if ban is not None and len(ban) > 0]
                print(f"LiteBans: {bans}\n")
            if url_type == 'MCBOUNCER':
                MCBouncerBans = await asyncio.gather(*[mcbouncer.handle_request(url.replace("<UUID>", PLAYER_UUID).replace("<UUID-DASH>", PLAYER_UUID_DASH), session) for url in external_urls[url_type]])
                print(f"MCBouncer: {MCBouncerBans}\n")
            if url_type == 'MCBANS':
                MCBansBans = await asyncio.gather(*[mcbans.handle_request(url.replace("<UUID>", PLAYER_UUID).replace("<UUID-DASH>", PLAYER_UUID_DASH), session) for url in external_urls[url_type]])
                bans = [ban for ban in MCBansBans if ban is not None and len(ban) > 0]
                print(f"MCBans: {bans}\n")
            if url_type == 'MCONLINE':
                MCOnlineBans = await asyncio.gather(*[mconline.handle_request(url.replace("<USERNAME>", PLAYER_USERNAME), session) for url in external_urls[url_type]])
                print(f"MCOnline: {MCOnlineBans}\n")
            if url_type == 'JOHNYMUFFIN':
                print(f"JohnnyMuffin: {external_urls[url_type]}\n")
            if url_type == 'MCCENTRAL':
                print(f"MCCentral: {external_urls[url_type]}\n")
            if url_type == 'MCBRAWL':
                print(f"MCBrawl: {external_urls[url_type]}\n")
            if url_type == 'COSMICPRISON':
                print(f"CosmicPrison: {external_urls[url_type]}\n")
            if url_type == 'STRONGCRAFT':
                print(f"StrongCraft: {external_urls[url_type]}\n")
            if url_type == 'MANACUBE':
                print(f"ManaCube: {external_urls[url_type]}\n")

# "USERNAME"
if __name__ == "__main__":
	asyncio.run(main())