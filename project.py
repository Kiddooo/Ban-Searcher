import os
import re
from typing import Optional, Tuple

from InquirerPy import prompt
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from banlist_project.pipelines import BanPipeline
from player_converter import Player, PlayerValidationError
from player_report import PlayerReport
from utils import logging


def get_user_input() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Prompts the user for input and returns the username, UUID,
    and UUID with dashes, or None values on failure.

    Returns:
        Tuple[Optional[str], Optional[str], Optional[str]]:
        A tuple containing the username, UUID, and UUID with dashes.
    """
    prompt_questions = [
        {
            "type": "list",
            "name": "type",
            "message": "What will you enter?",
            "choices": ["Username", "UUID"],
        },
        {"type": "input", "name": "value", "message": "Enter a value: "},
    ]
    user_input = prompt(prompt_questions)
    input_type = user_input["type"]
    input_value = user_input["value"].strip()

    if not input_value:
        raise ValueError(f"The input for {input_type} is invalid.")

    if input_type.lower() == "uuid":
        input_value = re.sub(r"-", "", input_value)

    try:
        player_data = {input_type.lower(): input_value}
        player = Player(**player_data)

        if player.username and player.uuid:
            return player.username, player.uuid, player.uuid_dash
        else:
            err_msg = f"Failed to fetch all player attributes. Username: {player.username}, UUID: {player.uuid}"
            raise ValueError(err_msg)
    except PlayerValidationError as e:
        raise ValueError(f"Validation error when creating a Player: {e}") from e


def clear_screen() -> None:
    """
    Clears the console screen.

    :return: None
    """
    # Determine the command based on the operating system
    command = "cls" if os.name == "nt" else "clear"
    # Execute the command to clear the screen
    os.system(command)  # nosec


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
        process.crawl(
            spider, username=username, player_uuid=uuid, player_uuid_dash=uuid_dash
        )

    process.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    clear_screen()

    player_username, player_uuid, player_uuid_dash = get_user_input()

    start_crawling_process(player_username, player_uuid, player_uuid_dash)

    player_report = PlayerReport(player_username, player_uuid_dash, BanPipeline.bans)
    player_report.generate_report()
