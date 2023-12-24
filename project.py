import os
from InquirerPy import prompt
from banlist_project.pipelines import BanPipeline
from utils import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from player_report import PlayerReport
from player_converter import Player
from pydantic import ValidationError

from typing import Tuple, Optional

def get_user_input() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Prompts the user for input and returns the username, UUID,
    and UUID with dashes, or None values on failure.

    Returns:
        Tuple[Optional[str], Optional[str], Optional[str]]:
        A tuple containing the username, UUID, and UUID with dashes.
    """
    user_prompt = [
        {
            'type': 'list', 'name': 'type',
            'message': 'What will you enter?',
            'choices': ['Username', 'UUID']
        }
    ]
    input_type = prompt(user_prompt)["type"]

    value_prompt = [
        {
            'type': 'input', 'name': 'value',
            'message': f'Enter a {input_type}: '
        }
    ]
    input_value = prompt(value_prompt)["value"]

    if not input_value:
        logging.error(f'The input for {input_type} is invalid.')
        return None, None, None

    if input_type.lower() == 'uuid':
        input_value = input_value.replace('-', '')

    try:
        player_data = {input_type.lower(): input_value}
        player = Player(**player_data)
        player.ensure_all_attributes()

        if player.username and player.uuid:
            return (player.username, player.uuid, player.uuid_dash)
        else:
            err_msg = \
                f'Failed to fetch all player attributes. ' \
                f'Username: {player.username}, UUID: {player.uuid}'
            logging.error(err_msg)
            return None, None, None
    except ValidationError as e:
        logging.error(f'Validation error when creating a Player: {e}')
        return None, None, None

def clear_screen() -> None:
    """
    Clears the console screen.

    :return: None
    """
    # Determine the command based on the operating system
    command = 'cls' if os.name == 'nt' else 'clear'
    # Execute the command to clear the screen
    os.system(command) #nosec

def start_crawling_process(username: str, uuid: str, uuid_dash: str) -> None:
    """
    Start the crawling process for the 'JohnyMuffinSpider'.

    Args:
    - username: str - The username to crawl data for.
    - uuid: str - The UUID associated with the username.
    - uuid_dash: str - The UUID with dashes associated with the username.

    :return: None

    """
    process = CrawlerProcess(get_project_settings())
    for spider in process.spider_loader.list():
        process.crawl(spider, username=username, player_uuid=uuid, player_uuid_dash=uuid_dash)

    process.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    clear_screen()

    player_username, player_uuid, player_uuid_dash = get_user_input()

    start_crawling_process(player_username, player_uuid, player_uuid_dash)

    player_report = PlayerReport(player_username, player_uuid_dash, BanPipeline.bans)
    player_report.generate_report()