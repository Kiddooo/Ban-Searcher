import os
import subprocess  # nosec
from typing import Optional, Tuple

from colorama import Fore, Style
from InquirerPy import prompt
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.pipelines import BanPipeline
from player_converter import Player, PlayerValidationError
from backend.player_report import PlayerReport
from backend.utils import logger


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
        input_value = input_value.replace("-", "")

    try:
        player_data = {input_type.lower(): input_value}
        player = Player(**player_data)
        player.ensure_all_attributes()

        if not (player.username and player.uuid):
            raise ValueError(
                f"Failed to fetch all player attributes. Username: {player.username}, UUID: {player.uuid}"
            )
        return player.username, player.uuid, player.uuid_dash
    except PlayerValidationError as e:
        raise ValueError(f"Validation error when creating a Player: {e}") from e


def clear_screen() -> None:
    """
    Clears the console screen.

    :return: None
    """
    try:
        # Determine the clear_screen_command based on the operating system
        clear_screen_command = "cls" if os.name == "nt" else "clear"
        # Execute the clear_screen_command to clear the screen
        return_code = subprocess.run(
            clear_screen_command, shell=True
        ).returncode  # nosec
        if return_code != 0:
            raise OSError(f"Failed to clear the screen. Return code: {return_code}")
    except Exception as e:
        print(f"An error occurred while clearing the screen: {e}")


def start_crawling_process(username: str, uuid: str, uuid_dash: str) -> None:
    """
    Start the crawling process.

    Args:
    - username: str - The username to crawl data for.
    - uuid: str - The UUID associated with the username.
    - uuid_dash: str - The UUID with dashes associated with the username.

    :return: None

    """
    process = CrawlerProcess(get_project_settings())
    for spider_name in process.spider_loader.list():
        process.crawl(
            spider_name,
            username=username,
            player_uuid=uuid,
            player_uuid_dash=uuid_dash,
        )

    process.start()


if __name__ == "__main__":
    clear_screen()

    player_username, player_uuid, player_uuid_dash = get_user_input()

    start_crawling_process(player_username, player_uuid, player_uuid_dash)

    logger.info(
        f"{Fore.GREEN} Finished crawling! Found {len(BanPipeline.bans)} bans. Opening Report...{Style.RESET_ALL}"
    )

    player_report = PlayerReport(
        player_username,
        player_uuid_dash,
        sorted(BanPipeline.bans, key=lambda x: x["source"]),
    )
    player_report.generate_report()
