import os
import re
import json
import sys
import time
from typing import List
import requests
import subprocess #nosec
import webbrowser
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from deep_translator import GoogleTranslator, single_detection
from banlist_project.items import BanItem
import logging

load_dotenv()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
FLARESOLVER_URL = 'http://localhost:8191/v1'
DETECTLANGUAGE_API_KEY = os.getenv('DETECTLANGUAGE_API_KEY')

logger = logging.getLogger('Ban-Scraper')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_language(text: str) -> str:
    """
    Detect the language of the given text using an external API.

    :param text: The text whose language is to be detected.
    :return: The detected language.
    """
    # Detect language with the provided API key
    detected_lang = single_detection(
        text, api_key=DETECTLANGUAGE_API_KEY
    )
    return detected_lang

def translate(text: str, from_lang: str = 'auto', to_lang: str = 'en') -> str:
    """
    Translate text from one language to another using Google's API.

    Args:
    text (str): The text to be translated.
    from_lang (str, optional): The source language code (e.g., 'fr').
        Defaults to 'auto' for auto-detection.
    to_lang (str, optional): The target language code (e.g., 'en').
        Defaults to 'en' for English.

    Returns:
    str: The translated text.
    """

    # Create a translator object with specified source and target.
    translator = GoogleTranslator(source=from_lang, target=to_lang)

    # Translate the text and return the result.
    return translator.translate(text)

def load_external_urls():
    """
    Load external URLs from a JSON file.

    Raises:
        FileNotFoundError: If the 'websites.json' file is not found.
        JSONDecodeError: If the file content is not valid JSON.
        Exception: For any other types of exceptions.

    Returns:
        A list or dict containing the data from 'websites.json'.
    """
    # Path to the JSON file containing the URLs
    json_path = "websites.json"
    try:
        # Open the file and load the JSON content
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError as e:
        msg = f"Error: {json_path} file not found."
        raise FileNotFoundError(msg) from e
    except json.JSONDecodeError as e:
        msg = f"Error: {json_path} is not valid JSON."
        raise json.JSONDecodeError(msg) from e
    except Exception as e:
        # Handle unexpected exceptions
        raise Exception(f"Unexpected error: {e}") from e

def generate_report(player_username, player_uuid, bans):
    """
    Generates a report for a player, writes it to a JSON file, and
    opens a local server to display the report in a browser.

    :param player_username: Username of the player
    :param player_uuid: UUID of the player with dashes
    :param bans: List of ban items for the player
    """
    # Construct the report dictionary
    ban_report = {
        "username": player_username,
        "uuid": player_uuid,
        "bans": bans,
        "totalbans": len(bans),
        "skinurl": "",
        "pastskins": ["", "", ""]
    }

    # Determine the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Define the directory to store the JSON report
    frontend_dir = os.path.join(script_dir, "SecretFrontend")

    # Create the full path to the JSON file
    bans_file = os.path.join(frontend_dir, "bans.json")

    # Write the report to the JSON file
    with open(bans_file, "w", encoding="utf-8") as bans_json:
        json.dump(ban_report, bans_json, indent=4, default=lambda obj: obj.to_json() if isinstance(obj, BanItem) else None)

    # Change working directory to the frontend directory
    os.chdir(frontend_dir)

    # Start a local HTTP server to serve the report
    server_cmd = [sys.executable, "-m", "http.server", "--bind", "127.0.0.1", "8000"]
    p = subprocess.Popen(server_cmd, stdout=subprocess.PIPE) # nosec

    # Open the report in the default web browser
    webbrowser.open("http://127.0.0.1:8000/index.html",
                    new=2, autoraise=True)

    # Wait for a short period before killing the server
    time.sleep(5)
    p.kill()

def check_response_text(response_text: str, search_strings: List[str]) -> bool:
    """
    Checks if any search string is in response_text.

    Args:
    response_text (str): Text to search in.
    search_strings (List[str]): Strings to search for.

    Returns:
    bool: True if any string found, False otherwise.
    """
    return any(re.search(string, response_text) for string in search_strings)

def get_player_skins(username=None, uuid=None):
    """
    Retrieves a list of skin IDs for a given Minecraft player.

    Args:
    username (str): Player's username.
    uuid (str): Player's UUID.

    Returns:
    list: Skin IDs associated with the player.
    """
    base_url = 'https://namemc.com/profile/'
    profile_url = f"{base_url}{username or uuid}"

    # Simplified headers and data dictionary
    headers = {'Content-Type': 'application/json'}
    data = {"cmd": "request.get", "url": profile_url, "maxTimeout": 60000}

    # Post request using a shorter timeout syntax
    response = requests.post(
        FLARESOLVER_URL, json=data, headers=headers, timeout=60
    )

    # Get the HTML content from the response
    html_content = response.json().get('solution', {}).get('response', '')

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get the script tags that contain skin IDs
    skin_scripts = soup.find_all(
        'script',
        attrs={'defer': ''},
        src=lambda x: "s.namemc.com/i/" in x if x else False
    )[:-1]

    # Extract skin IDs from the script tags
    skin_ids = [script['src'].split('/')[-1].replace('.js', '') for script in skin_scripts]

    return skin_ids