import os
import platform
import subprocess
from PyInquirer import prompt
from banlist_project.pipelines import BanPipeline
import utils
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from banlist_project.spiders.mccentral_spider import MCCentralSpider
from banlist_project.spiders.mundominecraft_spider import MundoMinecraftSpider
from banlist_project.spiders.banmanager_bonemeal_spider import BanManagerBonemealSpider
from banlist_project.spiders.banmanager_spider import BanManagerSpider
from banlist_project.spiders.cosmicgames_spider import CosmicGamesSpider
from banlist_project.spiders.cubeville_spider import CubevilleSpider
from banlist_project.spiders.cultcraft_spider import CultcraftSpider
from banlist_project.spiders.democracycraft_spider import DemocracycraftSpider
from banlist_project.spiders.guster_spider import GusterSpider
from banlist_project.spiders.johnymuffin_spider import JohnyMuffinSpider
from banlist_project.spiders.majncraft_spider import MajncraftSpider
from banlist_project.spiders.manacube_spider import ManaCubeSpider
from banlist_project.spiders.mcbans_spider import MCBansSpider
from banlist_project.spiders.mcbouncer_spider import MCBouncerSpider
from banlist_project.spiders.mcbrawl_spider import MCBrawlSpider
from banlist_project.spiders.mconline_spider import MCOnlineSpider
from banlist_project.spiders.snapcraft_spider import SnapcraftSpider
from banlist_project.spiders.strongcraft_spider import StrongcraftSpider
from banlist_project.spiders.syuu_spider import SyuuSpider
from banlist_project.spiders.litebans_spider import LiteBansSpider

# spiders = [MCCentralSpider, MundoMinecraftSpider, BanManagerBonemealSpider, BanManagerSpider, 
#            CosmicGamesSpider, CubevilleSpider, CultcraftSpider, 
#            DemocracycraftSpider, GusterSpider, JohnyMuffinSpider, 
#            MajncraftSpider, ManaCubeSpider, MCBansSpider, MCBouncerSpider, 
#            MCBrawlSpider, MCOnlineSpider, SnapcraftSpider, StrongcraftSpider, 
#            LiteBansSpider
# ]

def get_user_input():
    # Prompt user for username and validate it
    username = prompt([{'type': 'input', 'name': 'username', 'message': 'Enter a username: ', 'validate': utils.validateUsername}])["username"]

    # Convert username to UUID and UUID to UUID with dashes
    uuid = utils.UsernameToUUID(username)
    uuid_dash = utils.UUIDToUUIDDash(uuid)

    return username, uuid, uuid_dash

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    clear_screen()
    
    PLAYER_USERNAME, PLAYER_UUID, PLAYER_UUID_DASH = get_user_input()

    process = CrawlerProcess(get_project_settings())
    
    for spider in process.spider_loader.list():
        process.crawl(spider, username=PLAYER_USERNAME, player_uuid=PLAYER_UUID, player_uuid_dash=PLAYER_UUID_DASH)

    
    
    process.start()
    print(BanPipeline.bans)
    # utils.generate_report(PLAYER_USERNAME, PLAYER_UUID_DASH, BanPipeline.bans)
