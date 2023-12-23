import os
from PyInquirer import prompt
from banlist_project.pipelines import BanPipeline
from utils import generate_report, validate_input
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from player_converter import PlayerConverter


def get_user_input():
    input_type = prompt([{'type': 'list', 'name': 'type', 'message': 'What will you enter?', 'choices': ['Username', 'UUID', 'UUID with dashes']}])["type"]
    input_value = prompt([{'type': 'input', 'name': 'value', 'message': f'Enter a {input_type}: ', 'validate': validate_input}])["value"]

    converter = PlayerConverter(input_value, input_type)
    username, uuid, uuid_dash = converter.convert()

    return username, uuid, uuid_dash


def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear') #nosec


def start_crawling_process(username, uuid, uuid_dash):
    """
    Start the crawling process for each spider.
    """
    process = CrawlerProcess(get_project_settings())
    for spider in process.spider_loader.list():
        process.crawl(spider, username=username, player_uuid=uuid, player_uuid_dash=uuid_dash)

    process.start()


if __name__ == "__main__":
    clear_screen()
    player_username, player_uuid, player_uuid_dash = get_user_input()
    start_crawling_process(player_username, player_uuid, player_uuid_dash)
    generate_report(player_username, player_uuid_dash, BanPipeline.bans)