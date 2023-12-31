import logging
import os
import re
from datetime import datetime, timezone

import dateparser
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator, single_detection
from dotenv import load_dotenv

load_dotenv()
DETECTLANGUAGE_API_KEY = os.getenv("DETECTLANGUAGE_API_KEY")
FLARESOLVER_URL = "http://localhost:8191/v1"

logger = logging.getLogger("Ban-Scraper")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

class DateParsingError(Exception):
    pass


def parse_date(date_str: str, settings: dict):
    """
    Parses a date string and returns the corresponding date object.

    Parameters:
        date_str (str): The date string to be parsed.

    Returns:
        datetime.datetime or str: The parsed date object or "Permanent" if the ban is permanent.

    Raises:
        DateParsingError: If there is an error parsing the date.

    """
    try:
        if not isinstance(date_str, str):
            raise ValueError("date_str must be a string")

        date_str = re.sub(r"\bklo\b", "", date_str).split(" (")[0].strip()
        permanent_ban_types = {"Permanent Ban", "Permanentni", "Ban Permanente"}

        if date_str in permanent_ban_types:
            ban_expires = "Permanent"
        else:
            ban_expires = dateparser.parse(date_str, settings=settings)

        return ban_expires

    except Exception as e:
        logging.error(f"Error parsing date: {date_str}: {str(e)}")
        raise DateParsingError(
            f"Error parsing date: {date_str}: {str(e)}"
        ) from DateParsingError


def calculate_timestamp(date):
    """
    Calculates the timestamp from a given date.

    Parameters:
        date: The date to calculate the timestamp from.

    Returns:
        int or str: The calculated timestamp as an integer or "N/A" if the date is None.
    """
    if date is None:
        return "N/A"
    elif isinstance(date, str):
        return date
    elif isinstance(date, datetime):
        return int(date.replace(tzinfo=timezone.utc).timestamp())
    else:
        raise TypeError("Invalid input type for `date`")


def get_language(text: str) -> str:
    """
    Detects the language of a given text using an API key.

    Args:
        text (str): The text for which the language needs to be detected.
        api_key (str): The API key for language detection.

    Returns:
        str: The detected language of the input text, or a default value/error message if language detection fails.
    """
    try:
        if not text:
            return "Text argument is empty"

        if not isinstance(text, str):
            raise TypeError("The 'text' argument must be a string.")

        # Detect language with the provided API key
        detected_lang = single_detection(text, api_key=DETECTLANGUAGE_API_KEY)
        return detected_lang
    except Exception as e:
        return "Language detection failed: " + str(e)


def translate(text: str, from_lang: str = "auto", to_lang: str = "en") -> str:
    """
    Translates text from one language to another using the GoogleTranslator class from the deep_translator library.

    Args:
        text (str): The text to be translated.
        from_lang (str, optional): The source language of the text. Defaults to 'auto', which automatically detects the language.
        to_lang (str, optional): The target language for the translation. Defaults to 'en' (English).

    Returns:
        str: The translated text in the target language.
    """
    try:
        if not isinstance(text, str):
            raise TypeError("The 'text' argument must be a string.")

        if not text:
            return ""

        # Create a translator object with specified source and target.
        translator = GoogleTranslator(source=from_lang, target=to_lang)

        # Translate the text and return the result.
        return translator.translate(text)
    except Exception as e:
        return "Translation failed: " + str(e)


def get_player_skins(username=None, uuid=None):
    """
    Retrieves skin IDs associated with a Minecraft player's profile.

    Args:
        username (str, optional): The username of the Minecraft player. If not provided, `uuid` must be provided.
        uuid (str, optional): The UUID of the Minecraft player. If not provided, `username` must be provided.

    Returns:
        list: A list of skin IDs associated with the Minecraft player's profile.
    """
    base_url = "https://namemc.com/profile/"
    profile_url = f"{base_url}{username or uuid}"

    # Simplified headers and data dictionary
    headers = {"Content-Type": "application/json"}
    data = {"cmd": "request.get", "url": profile_url, "maxTimeout": 60000}

    # Post request using a shorter timeout syntax
    response = requests.post(FLARESOLVER_URL, json=data, headers=headers, timeout=60)

    # Get the HTML content from the response
    html_content = response.json().get("solution", {}).get("response", "")

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Get the script tags that contain skin IDs
    skin_scripts = soup.select('script[src*="s.namemc.com/i/"]')[:-1]

    # Extract skin IDs from the script tags
    skin_ids = [
        script["src"].split("/")[-1].replace(".js", "") for script in skin_scripts
    ]

    return skin_ids
