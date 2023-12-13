import os
from PyInquirer import prompt
from banlist_project.pipelines import BanPipeline
import utils
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def get_user_input():
    """
    Prompt the user for a username and validate it.
    Convert the username to UUID and UUID to UUID with dashes.
    """
    username = prompt([{'type': 'input', 'name': 'username', 'message': 'Enter a username: ', 'validate': utils.validate_username}])["username"]
    uuid = utils.username_to_uuid(username)
    uuid_dash = utils.uuid_to_uuid_dash(uuid)
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
    utils.generate_report(player_username, player_uuid_dash, BanPipeline.bans)