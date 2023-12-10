import sys
import utils
import os
import subprocess  # nosec
import platform
import webbrowser
import time
from tqdm import tqdm
import concurrent.futures
from PyInquirer import prompt
import webpages

# Constants
CONSTANT_UUID: str = "<UUID>"
CONSTANT_UUID_DASH: str = "<UUID-DASH>"
CONSTANT_USERNAME: str = "<USERNAME>"
MAX_WORKERS = 25


def main(PLAYER_USERNAME, PLAYER_UUID, PLAYER_UUID_DASH):
    external_urls = utils.load_external_urls()
    _bans = []
    url_types = {
        "LITEBANS": (webpages.LiteBansHandler, CONSTANT_UUID, PLAYER_UUID),
        "LITEBANS_UUID_DASH": (webpages.LiteBansHandler, CONSTANT_UUID_DASH, PLAYER_UUID_DASH),
        "MCBOUNCER": (webpages.MCBouncerHandler, CONSTANT_UUID, PLAYER_UUID),
        "MCBANS": (webpages.MCBansHandler, CONSTANT_UUID, PLAYER_UUID),
        "MCONLINE": (webpages.MCOnlineHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        "JOHNYMUFFIN": (webpages.JohnyMuffinHandler, CONSTANT_UUID_DASH, PLAYER_UUID_DASH),
        "MCCENTRAL": (webpages.MCCentralHandler, CONSTANT_UUID, PLAYER_UUID),
        "MCBRAWL": (webpages.MCBrawlHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        "COSMICPRISON": (webpages.CosmicGamesHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        "STRONGCRAFT": (webpages.StrongcraftHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        "MANACUBE": (webpages.ManaCubeHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        "SNAPCRAFT": (webpages.SnapcraftHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        "CUBEVILLE": (webpages.CubevilleHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        "GUSTER": (webpages.GusterHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        'DEMOCRACYCRAFT': (webpages.DemocracycraftHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        "SYUU": (webpages.SyuuHandler, CONSTANT_UUID_DASH, PLAYER_UUID_DASH),
        'MAJNCRAFT': (webpages.MajncraftHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        'CULTCRAFT': (webpages.CultcraftHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        'BANMANAGER': (webpages.BanManagerHandler, CONSTANT_USERNAME, PLAYER_USERNAME),
        'BANMANAGER_BONEMEAL': (webpages.BanManagerBonemealHandler, CONSTANT_UUID, PLAYER_UUID),
        'MUNDOMINECRAFT': (webpages.MundoMinecraftHandler, CONSTANT_UUID_DASH, PLAYER_UUID_DASH),
    }

    start_time = time.time()

    tasks = []
    for url_type, (HandlerClass, replacement, value) in url_types.items():
        for url in external_urls[url_type]:
            url = url.replace(replacement, value)
            handler = HandlerClass()
            tasks.append((handler.handle_request, url))

    print(f"Searching {len(tasks)} URLs for bans...")

    futures_to_urls = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(handle_request, url) for handle_request, url in tasks]
        for future, task in zip(futures, tasks):
            futures_to_urls[future] = task[1]  # Store the URL associated with the future

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing URLs"):
            url = futures_to_urls[future]  # Get the URL associated with the future
            bans = future.result(timeout=None)
            if bans is not None and len(bans) != 0:
                _bans.extend(bans)

    utils.generate_report(PLAYER_USERNAME, PLAYER_UUID_DASH, _bans)

    end_time = time.time()
    print(f"Took {int(end_time - start_time)} seconds to generate")
    print("Opening report...")
    os.chdir("SecretFrontend")
    p = subprocess.Popen([sys.executable, "-m", "http.server", "--bind", "127.0.0.1", "8000"], stdout=subprocess.PIPE) # nosec
    webbrowser.open("http://127.0.0.1:8000/index.html", new=2, autoraise=True)
    time.sleep(5)
    p.kill()


if __name__ == "__main__":
    if platform.system() == 'Windows':
        subprocess.run('cls', shell=True, check=True)  # nosec
    else:
        subprocess.run('clear', shell=True, check=True)  # nosec
    PLAYER_USERNAME = prompt([{'type': 'input', 'name': 'username', 'message': 'Enter a username: ', 'validate': utils.validateUsername}])["username"]
    PLAYER_UUID = utils.UsernameToUUID(PLAYER_USERNAME)
    PLAYER_UUID_DASH = utils.UUIDToUUIDDash(PLAYER_UUID)
    main(PLAYER_USERNAME, PLAYER_UUID, PLAYER_UUID_DASH)
