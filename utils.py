import subprocess
import sys
import time
import webbrowser
import requests
import re
import traceback
import json
import os
from deep_translator import GoogleTranslator, single_detection
from dotenv import load_dotenv

from banlist_project.items import BanItem

load_dotenv()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
FLARESOLVER_URL = 'http://localhost:8191/v1'
DETECTLANGUAGE_API_KEY = os.getenv('DETECTLANGUAGE_API_KEY')

def get_language(text: str) -> str:
    lang = single_detection(text, api_key=DETECTLANGUAGE_API_KEY)
    return lang

def translate(text: str, from_lang = 'auto', to_lang = 'en') -> str:
    translated = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
    return translated

def load_external_urls():
    try:
        with open("websites.json", "r") as external_json_urls:
            return json.load(external_json_urls)
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: websites.json file not found.") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("Error: websites.json is not a valid JSON file.") from e
    except Exception as e:
        raise Exception(f"Unexpected error: {e}") from e

def generate_report(PLAYER_USERNAME, PLAYER_UUID_DASH, _bans):
    print(os.getcwd())
    ban_report = {
        "username": PLAYER_USERNAME,
        "uuid": PLAYER_UUID_DASH,
        "bans": _bans,
        "totalbans": len(_bans),
        "skinurl": "",
        "pastskins": ["", "", ""]
    }
    # Get the directory of the current Python script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Get the absolute path to the SecretFrontend directory
    secret_frontend_dir = os.path.join(script_dir, "SecretFrontend")
    # Construct the full path to the bans.json file
    bans_file = os.path.join(secret_frontend_dir, "bans.json")
    with open(bans_file, "w", encoding="utf-8") as bans_json:
        json.dump(ban_report, bans_json, indent=4, default=lambda obj: obj.to_json() if isinstance(obj, BanItem) else None)
    
    print("Opening report...")
    os.chdir(secret_frontend_dir)
    p = subprocess.Popen([sys.executable, "-m", "http.server", "--bind", "127.0.0.1", "8000"], stdout=subprocess.PIPE) # nosec
    webbrowser.open("http://127.0.0.1:8000/index.html", new=2, autoraise=True)
    time.sleep(5)
    p.kill()

def validateUsername(Username: str) -> str:
	try:
		conversion = requests.get("https://api.mojang.com/users/profiles/minecraft/" + Username, timeout=5).json()
		if conversion["id"]:
			return True
	except KeyError:
		return 'Invalid Username'

def UUIDToUsername(UUID: str) -> str:
	try:
		conversion = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/{UUID}", timeout=5).json()
		return conversion["name"]

	except KeyError:
		print("DUN")


def UsernameToUUID(Username: str) -> str:
	try:
		conversion = requests.get("https://api.mojang.com/users/profiles/minecraft/" + Username, timeout=5).json()
		return conversion["id"]
	except KeyError:
		return traceback.format_exc()


def UUIDToUUIDDash(UUID: str) -> str:
	matcher = re.search(
		"([a-f0-9]{8})([a-f0-9]{4})([0-5][0-9a-f]{3})([089ab][0-9a-f]{3})([0-9a-f]{12})",
		UUID,
	)
	return f"{matcher.group(1)}-{matcher.group(2)}-{matcher.group(3)}-{matcher.group(4)}-{matcher.group(5)}"


def check_response_text(response_text, search_strings):
	for string in search_strings:
		if re.search(string, response_text):
			return True
	return False


# def playerSkins(current=False, username=False, uuid=False): #username or uuid is 'false' because its not mandatory to enter them11
# 	if isinstance(username, str):
# 		url = 'https://namemc.com/profile/' + username#gets websites code or scrapes it

# 	if isinstance(uuid, str):
# 		url = 'https://namemc.com/profile/' + str(uuid) #gets websites code or scrapes it

# 	headers = {'Content-Type': 'application/json'}

# 	data = {
# 		"cmd": "request.get",
# 		"url": f"{url}",
# 		"maxTimeout": 60000
# 	}

# 	response = requests.post(FLARESOLVER_URL, data=json.dumps(data), headers=headers, timeout=60)
# 	html = response.json().get('solution').get('response')
# 	soup = BeautifulSoup(html, 'html.parser')
# 	skins = soup.find_all('script', attrs={'defer': ''}, src=lambda x: "s.namemc.com/i/" in x if x else False)[:-1]
# 	skin_ids = []

# 	for skin in skins:
# 		skin = str(skin).replace("<script defer=\"\" src=\"https://s.namemc.com/i/", "").replace(".js\"></script>", "")
# 		skin_ids.append(skin)

# 	return skin_ids