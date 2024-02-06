from colorama import Fore, Style
import logging


class BanPipeline:
    bans = []

    def __init__(self):
        """
        Initializes a new instance of the BanPipeline class.

        Inputs:
        - None

        Outputs:
        - None
        """
        self.logger = logging.getLogger("Ban-Scraper")
        self.username = None
        self.player_uuid = None
        self.player_uuid_dash = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        Create an instance of the BanPipeline class.

        Args:
            crawler (object): The crawler object.

        Returns:
            BanPipeline: An instance of the BanPipeline class.
        """
        return cls()

    def open_spider(self, spider):
        """
        Initializes the instance variables `username`, `player_uuid`, and `player_uuid_dash` with values from the `spider` object.

        Args:
            spider (object): The spider object that contains player information.

        Example Usage:
            # Create an instance of the BanPipeline class
            pipeline = BanPipeline()

            # Create a spider object with player information
            spider = Spider(player_username='john_doe', player_uuid='1234567890', player_uuid_dash='1234-5678-90')

            # Call the open_spider method to initialize the instance variables
            pipeline.open_spider(spider)

            # Access the initialized instance variables
            print(pipeline.username)  # Output: john_doe
            print(pipeline.player_uuid)  # Output: 1234567890
            print(pipeline.player_uuid_dash)  # Output: 1234-5678-90

        """
        self.username = spider.player_username
        self.player_uuid = spider.player_uuid
        self.player_uuid_dash = spider.player_uuid_dash
        self.logger.info(f"{Fore.BLUE}Starting spider: {spider.name}{Style.RESET_ALL}")

    def process_item(self, item, spider):
        """
        Process the input item and append it to the bans list.

        Args:
            item (dict): The item to be processed by the pipeline.
            spider (object): The spider object associated with the item.

        Returns:
            dict: The same item that was passed as input.
        """
        self.logger.info(
            f"{Fore.MAGENTA}{spider.name} | Found ban from source: {item.get('source')}{Style.RESET_ALL}"
        )
        self.bans.append(item)
        return item

    def get_bans(self):
        return self.bans
