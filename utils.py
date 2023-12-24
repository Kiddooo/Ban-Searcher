import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from deep_translator import GoogleTranslator, single_detection
import logging

load_dotenv()
DETECTLANGUAGE_API_KEY = os.getenv('DETECTLANGUAGE_API_KEY')
FLARESOLVER_URL = 'http://localhost:8191/v1'

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