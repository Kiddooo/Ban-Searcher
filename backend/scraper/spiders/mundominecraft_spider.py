import json
from enum import Enum

import scrapy
import tldextract
from colorama import Fore, Style

from backend.utils import get_language, logger, translate
from scraper.items import BanItem

# Constants for repeated strings
PLAYER_BANS = "playerBans"
LIST_PLAYER_PUNISHMENT_RECORDS = "listPlayerPunishmentRecords"
PERMANENT_BAN_EXPIRY = 0


# Enum for ban types
class BanType(Enum):
    PLAYER_BANS = PLAYER_BANS
    LIST_PLAYER_PUNISHMENT_RECORDS = LIST_PLAYER_PUNISHMENT_RECORDS


# Spider class
class MundoMinecraftSpider(scrapy.Spider):
    name = "MundoMinecraftSpider"

    headers = {
        "Accept": "application/json",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://mundo-minecraft.com:3000",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }

    queries = {
        LIST_PLAYER_PUNISHMENT_RECORDS: {
            "query": "query listPlayerPunishmentRecords($serverId: ID!, $player: UUID!, $type: RecordType!, $limit: Int, $offset: Int) {listPlayerPunishmentRecords(serverId: $serverId, player: $player, type: $type, limit: $limit, offset: $offset) {total records {... on PlayerBanRecord {id actor {id name} pastActor {id name} created pastCreated reason expired acl {delete}} } server {id name}}}",
            "variables": {},
        },
        PLAYER_BANS: {
            "query": "query playerBans($id: UUID!) {\n  playerBans(player: $id) {\n    id\n    actor {\n      id\n      name\n    }\n    reason\n    created\n    updated\n    expires\n    acl {\n      update\n      delete\n    }\n    server {\n      id\n      name\n    }\n  }\n}",
            "variables": {},
        },
    }

    # Initialize the spider with username and UUIDs
    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if not all([username, player_uuid, player_uuid_dash]):
            raise ValueError("Invalid parameters")

        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    # Start the requests
    def start_requests(self):
        url = "http://mundo-minecraft.com:3000/graphql"
        self.headers["Referer"] = (
            "http://mundo-minecraft.com:3000/player/" + self.player_uuid_dash
        )
        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
        )
        for query_type, query in self.queries.items():
            data = query.copy()
            data["variables"] = self.get_query_variables(
                query_type, self.player_uuid_dash
            )
            yield scrapy.Request(
                url,
                method="POST",
                body=json.dumps(data),
                headers=self.headers,
                callback=self.parse,
                cb_kwargs=dict(query_type=query_type),
            )

    def parse(self, response, query_type):
        json_response = response.json()
        data = json_response.get("data")
        if data is not None:
            player_bans = data.get(BanType.PLAYER_BANS.value)
            if player_bans:
                yield from (
                    self.create_ban_item(ban, response.url) for ban in player_bans
                )
            punishment_records = data.get(BanType.LIST_PLAYER_PUNISHMENT_RECORDS.value)
            if punishment_records:
                records = punishment_records.get("records")
                yield from (
                    self.create_ban_item(record, response.url) for record in records
                )

    def create_ban_item(self, ban: dict, url: str) -> BanItem:
        source = "mundominecraft"
        ban_reason = ban["reason"]
        reason = (
            translate(ban_reason) if get_language(ban_reason) != "en" else ban_reason
        )
        try:
            if ban["expired"]:
                expires = ban["created"]
                date = ban["pastCreated"]
        except KeyError:
            expires = (
                "Permanent"
                if ban["expires"] == PERMANENT_BAN_EXPIRY
                else ban["expires"]
            )
            date = ban["created"]

        return BanItem(
            {
                "source": source,
                "url": url,
                "reason": reason,
                "date": date,
                "expires": expires,
            }
        )

    def get_query_variables(self, type: str, user_uuid: str) -> dict:
        variables = {
            "listPlayerPunishmentRecords": {
                "activePage": 1,
                "limit": 20,
                "offset": 0,
                "serverId": "4044b44c",
                "player": user_uuid,
                "type": "PlayerBanRecord",
            },
            "playerBans": {"id": user_uuid},
        }
        return variables.get(type, {})
