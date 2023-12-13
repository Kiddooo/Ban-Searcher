import scrapy
from banlist_project.items import BanItem
from enum import Enum
import json
from utils import get_language, translate

# Constants for repeated strings
PLAYER_BANS = 'playerBans'
LIST_PLAYER_PUNISHMENT_RECORDS = 'listPlayerPunishmentRecords'
PERMANENT_BAN_EXPIRY = 0

# Enum for ban types
class BanType(Enum):
    PLAYER_BANS = PLAYER_BANS
    LIST_PLAYER_PUNISHMENT_RECORDS = LIST_PLAYER_PUNISHMENT_RECORDS

# Spider class
class MundoMinecraftSpider(scrapy.Spider):
    name = 'MundoMinecraftSpider'
    # Headers for the requests
    headers = {
        "Accept": "application/json",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://mundo-minecraft.com:3000",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    # Queries for the requests
    queries = {
        LIST_PLAYER_PUNISHMENT_RECORDS: {
            "query": "query listPlayerPunishmentRecords($serverId: ID!, $player: UUID!, $type: RecordType!, $limit: Int, $offset: Int) {listPlayerPunishmentRecords(serverId: $serverId, player: $player, type: $type, limit: $limit, offset: $offset) {total records {... on PlayerBanRecord {id actor {id name} pastActor {id name} created pastCreated reason expired acl {delete}} } server {id name}}}",
            "variables": {}
        },
        PLAYER_BANS: {
            "query": "query playerBans($id: UUID!) {\n  playerBans(player: $id) {\n    id\n    actor {\n      id\n      name\n    }\n    reason\n    created\n    updated\n    expires\n    acl {\n      update\n      delete\n    }\n    server {\n      id\n      name\n    }\n  }\n}",
            "variables": {}
        }
    }

    # Initialize the spider with username and UUIDs
    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(MundoMinecraftSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    # Start the requests
    def start_requests(self):
        url = "http://mundo-minecraft.com:3000/graphql"
        self.headers["Referer"] = "http://mundo-minecraft.com:3000/player/" + self.player_uuid_dash
        for query_type in self.queries:
            data = self.queries[query_type].copy()  # create a copy of the query
            data["variables"] = self.get_query_variables(query_type, self.player_uuid_dash)  # get the variables for the query
            yield scrapy.Request(url, method='POST', body=json.dumps(data), headers=self.headers, callback=self.parse, cb_kwargs=dict(query_type=query_type))

    # Parse the response
    def parse(self, response, query_type):
        json_response = json.loads(response.text)
        if json_response['data'] is not None:
            if json_response['data'].get(BanType.PLAYER_BANS.value):
                bans = json_response['data'][BanType.PLAYER_BANS.value]
                yield from (self.create_ban_item(ban, response.url) for ban in bans)
            if json_response['data'].get(BanType.LIST_PLAYER_PUNISHMENT_RECORDS.value):
                bans = json_response['data'][BanType.LIST_PLAYER_PUNISHMENT_RECORDS.value]['records']
                yield from (self.create_ban_item(ban, response.url) for ban in bans)

    # Create a ban item
    def create_ban_item(self, ban, url):
        return BanItem({
            'source': 'mundominecraft',
            'url': url,
            'reason': translate(ban['reason']) if get_language(ban['reason']) != 'en' else ban['reason'],
            'date': ban['created'],
            'expires': "Permanent" if ban['expires'] == PERMANENT_BAN_EXPIRY else ban['expires']
        })

    # Get the variables for the query
    def get_query_variables(self, type, user_uuid):
        variables = {
            LIST_PLAYER_PUNISHMENT_RECORDS: {
                "activePage": 1,
                "limit": 20,
                "offset": 0,
                "serverId": "4044b44c",
                "player": user_uuid,
                "type": "PlayerBanRecord"
            },
            PLAYER_BANS: {"id": user_uuid}
        }
        return variables.get(type, {})