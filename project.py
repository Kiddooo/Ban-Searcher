import json
import utils
from webpages import litebans, mcbouncer, mcbans, mconline, johnmuffin, mccentral, cosmicgames, mcbrawl, snapcraft, cubeville, guster, strongcraft, manacube
from aiohttp import ClientSession
import asyncio
import os
from tqdm.asyncio import tqdm_asyncio

PLAYER_USERNAME = input("Enter a username: ")
PLAYER_UUID = utils.UsernameToUUID(PLAYER_USERNAME)
PLAYER_UUID_DASH = utils.UUIDToUUIDDash(PLAYER_UUID)

with open("websites.json", "r") as external_json_urls:
    external_urls = json.load(external_json_urls)


async def main():
    _bans = []
    url_types = {
        "LITEBANS": (litebans.handle_request, "<UUID>", PLAYER_UUID),
        "LITEBANS_UUID_DASH": (litebans.handle_request, "<UUID-DASH>", PLAYER_UUID_DASH),
        "MCBOUNCER": (mcbouncer.handle_request, "<UUID>", PLAYER_UUID),
        "MCBANS": (mcbans.handle_request, "<UUID>", PLAYER_UUID),
        "MCONLINE": (mconline.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "JOHNYMUFFIN": (johnmuffin.handle_request, "<UUID-DASH>", PLAYER_UUID_DASH),
        "MCCENTRAL": (mccentral.handle_request, "<UUID>", PLAYER_UUID),
        "MCBRAWL": (mcbrawl.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "COSMICPRISON": (cosmicgames.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "STRONGCRAFT": (strongcraft.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "MANACUBE": (manacube.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "SNAPCRAFT": (snapcraft.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "CUBEVILLE": (cubeville.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "GUSTER": (guster.handle_request, "<USERNAME>", PLAYER_USERNAME)
    }
    async with ClientSession(headers={"User-Agent": utils.USER_AGENT}) as session:
        for url_type, (handle_request, replacement, value) in url_types.items():
            bans = await tqdm_asyncio.gather(*[handle_request(url.replace(replacement, value), session) for url in external_urls[url_type]])
            for ban in bans:
                if ban is not None and len(ban) != 0:
                    _bans.extend(ban)

    ban_report = {
        "username": PLAYER_USERNAME, 
        "uuid": PLAYER_UUID_DASH, 
        "bans": _bans, 
        "totalbans": len(_bans),
        "skinurl": "",
        "pastskins": ["", "", ""]
    }
    with open("bans.json", "w", encoding="utf-8") as bans_json:
        json.dump(ban_report, bans_json, indent=4)
if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    asyncio.run(main())
