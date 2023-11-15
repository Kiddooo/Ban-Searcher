import requests
import json
import re
import utils
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
from webpages import website1, website2, website3, website4
import urllib.parse

PLAYER_USERNAME = input("Enter a username: ")
PLAYER_UUID = utils.UsernameToUUID(PLAYER_USERNAME)
PLAYER_UUID_DASH = utils.UUIDToUUIDDash(PLAYER_UUID)

with open("a.json", "r") as external_json_urls:
   external_urls = json.load(external_json_urls)


# def check_uuid_url(url):
# 	try:
# 		UUID_REQUEST = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}, cookies={"_cosmic_auth": "f8c9391e30d6ea3d8c849ec2a36fd7d8"})
# 		search_strings = ["has not joined", "not found in database", "<strong>Unknown User</strong>", f"The requested URL /u/{PLAYER_UUID}/ was not found on this server", "^$", "offence_count\":0", "No punishments found.", "404 Not Found", "No ha entrado al servidor.", "Non è mai entrato.", "Database error", "Error code 523", "Origin is unreachable"]
# 		if utils.check_response_text(UUID_REQUEST.text, search_strings):
# 			pass
		
# 		elif re.search("Recent Punishment for", UUID_REQUEST.text):
# 			tqdm.write("Potential Ban(s) For " + PLAYER_USERNAME + " - " + url)
# 		elif re.search("Recent Punishments for", UUID_REQUEST.text):
# 			tqdm.write("Potential Ban(s) For " + PLAYER_USERNAME + " - " + url)
# 		else:
# 			tqdm.write("Potential Ban(s) For " + PLAYER_USERNAME + " - " + url)
# 	except TimeoutError:
# 		pass
# 	except requests.exceptions.ConnectTimeout:
# 		pass
			
# def check_username_url(url):
# 	try:
# 		USERNAME_REQUEST = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}, cookies={"_cosmic_auth": "f8c9391e30d6ea3d8c849ec2a36fd7d8"})
# 		search_strings = ["NOTFOUND", "Player doesn't exist.", "There are no punishments under the account of .", "This user is not a player on our network!", "This user is not a JartexNetwork player!", "NOTBANNED", "Here you can look for the profile of any player on our network.", "\\[]", "No infractions were found for this category", "Error code 523", "Origin is unreachable"]
# 		if utils.check_response_text(USERNAME_REQUEST.text, search_strings):
# 			pass
		
# 		elif re.search("Recent Punishment for", USERNAME_REQUEST.text):
# 			tqdm.write("Potential Ban(s) For " + PLAYER_USERNAME + " - " + url)
# 		elif re.search("Recent Punishments for", USERNAME_REQUEST.text):
# 			tqdm.write("Potential Ban(s) For " + PLAYER_USERNAME + " - " + url)
# 		else:
# 			tqdm.write("Potential Ban(s) For " + PLAYER_USERNAME + " - " + url)
# 	except TimeoutError:
# 		pass
# 	except requests.exceptions.ConnectTimeout:
# 		pass


for url_type in external_urls:
	match url_type:
		case "LITEBANS":
			LiteBansBans = thread_map(website1.handle_request, [url.replace("<UUID>", PLAYER_UUID).replace("<UUID-DASH>", PLAYER_UUID_DASH) for url in external_urls[url_type]])
			print([ban for ban in LiteBansBans if ban is not None and len(ban) > 0])
		# case 'USERNAME':
		# 	UsernameBans = thread_map(website2.)