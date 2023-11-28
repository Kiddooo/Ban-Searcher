import json
import utils
from webpages import litebans, mcbouncer, mcbans, mconline, johnymuffin, mccentral, cosmicgames, mcbrawl, snapcraft, cubeville, guster, strongcraft, manacube
from multiprocessing.dummy import Pool as ThreadPool
import os
import subprocess
import webbrowser
import time
import concurrent

PLAYER_USERNAME = input("Enter a username: ")
PLAYER_UUID = utils.UsernameToUUID(PLAYER_USERNAME)
PLAYER_UUID_DASH = utils.UUIDToUUIDDash(PLAYER_UUID)

with open("websites.json", "r") as external_json_urls:
    external_urls = json.load(external_json_urls)

def main():
    _bans = []
    url_types = {
        "LITEBANS": (litebans.handle_request, "<UUID>", PLAYER_UUID),
        "LITEBANS_UUID_DASH": (litebans.handle_request, "<UUID-DASH>", PLAYER_UUID_DASH),
        "MCBOUNCER": (mcbouncer.handle_request, "<UUID>", PLAYER_UUID),
        "MCBANS": (mcbans.handle_request, "<UUID>", PLAYER_UUID),
        "MCONLINE": (mconline.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "JOHNYMUFFIN": (johnymuffin.handle_request, "<UUID-DASH>", PLAYER_UUID_DASH),
        "MCCENTRAL": (mccentral.handle_request, "<UUID>", PLAYER_UUID),
        "MCBRAWL": (mcbrawl.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "COSMICPRISON": (cosmicgames.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "STRONGCRAFT": (strongcraft.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "MANACUBE": (manacube.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "SNAPCRAFT": (snapcraft.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "CUBEVILLE": (cubeville.handle_request, "<USERNAME>", PLAYER_USERNAME),
        "GUSTER": (guster.handle_request, "<USERNAME>", PLAYER_USERNAME)
    }
    
    start_time = time.time()

    tasks = []
    for url_type, (handle_request, replacement, value) in url_types.items():
        for url in external_urls[url_type]:
            url = url.replace(replacement, value)
            tasks.append((handle_request, url))

    futures_to_urls = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(handle_request, url) for handle_request, url in tasks]
        for future, task in zip(futures, tasks):
            futures_to_urls[future] = task[1]  # Store the URL associated with the future

        for future in concurrent.futures.as_completed(futures):
            url = futures_to_urls[future]  # Get the URL associated with the future
            # print(f"Future from URL: {url}")
            bans = future.result()
            if bans is not None and len(bans) != 0:
                _bans.extend(bans)

    ban_report = {
        "username": PLAYER_USERNAME,
        "uuid": PLAYER_UUID_DASH,
        "bans": _bans,
        "totalbans": len(_bans),
        "skinurl": "",
        "pastskins": ["", "", ""]
    }
    with open("SecretFrontend/bans.json", "w", encoding="utf-8") as bans_json:
        json.dump(ban_report, bans_json, indent=4)

    end_time = time.time()
    print(f"Took {end_time - start_time} seconds to generate")
    print("Opening report...")
    subprocess.Popen(["python", "-m", "http.server", "--bind", "127.0.0.1", "--directory", "SecretFrontend"])
    webbrowser.open("http://127.0.0.1:8000/index.html", new=2, autoraise=True)

if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    main()
