import requests
import re
import traceback
from tqdm import tqdm
from bs4 import BeautifulSoup
import json


def UUIDToUsername(UUID: str) -> str:
	try:
		conversion = requests.get(
			"https://sessionserver.mojang.com/session/minecraft/profile/acfcb375e3064acfae8741bccb609557"
		).json()
		return conversion["name"]

	except Exception as e:
		print(traceback.format_exc())


def UsernameToUUID(Username: str) -> str:
	try:
		conversion = requests.get(
			"https://api.mojang.com/users/profiles/minecraft/" + Username
		).json()
		return conversion["id"]
	except Exception as e:
		print(traceback.format_exc())


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


def playerSkins(current=False, username=False, uuid=False): #username or uuid is 'false' because its not mandatory to enter them11
	base_url = 'http://localhost:8191/v1'

	if isinstance(username, str):
		url = 'https://namemc.com/profile/' + username#gets websites code or scrapes it

	if isinstance(uuid, str):
		url = 'https://namemc.com/profile/' + str(uuid) #gets websites code or scrapes it

	headers = {'Content-Type': 'application/json'}

	data = {
		"cmd": "request.get",
		"url": f"{url}",
		"maxTimeout": 60000
	}

	response = requests.post(base_url, data=json.dumps(data), headers=headers)
	html = response.json().get('solution').get('response')
	soup = BeautifulSoup(html, 'html.parser')
	skins = soup.find_all('script', attrs={'defer': ''}, src=lambda x: "s.namemc.com/i/" in x if x else False)[:-1]
	skin_ids = []

	for skin in skins:
		skin = str(skin).replace("<script defer=\"\" src=\"https://s.namemc.com/i/", "").replace(".js\"></script>", "")
		skin_ids.append(skin)

	return skin_ids