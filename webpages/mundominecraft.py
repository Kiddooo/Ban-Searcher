from WebsiteBaseHandler import BaseHandler
import requests
from tqdm import tqdm
import json
from utils import get_language, translate
from enum import Enum

class BanType(Enum):
    PLAYER_BANS = 'playerBans'
    LIST_PLAYER_PUNISHMENT_RECORDS = 'listPlayerPunishmentRecords'

PERMANENT_BAN_EXPIRY = 0

class MundoMinecraftHandler(BaseHandler):
    headers = {
        "Accept": "application/json",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://mundo-minecraft.com:3000",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    queries = {
        'listPlayerPunishmentRecords': {
            "query": "query listPlayerPunishmentRecords($serverId: ID!, $player: UUID!, $type: RecordType!, $limit: Int, $offset: Int) {listPlayerPunishmentRecords(serverId: $serverId, player: $player, type: $type, limit: $limit, offset: $offset) {total records {... on PlayerBanRecord {id actor {id name} pastActor {id name} created pastCreated reason expired acl {delete}} } server {id name}}}",
            "variables": {}
        },
        'playerBans': {
            "query": "query playerBans($id: UUID!) {\n  playerBans(player: $id) {\n    id\n    actor {\n      id\n      name\n    }\n    reason\n    created\n    updated\n    expires\n    acl {\n      update\n      delete\n    }\n    server {\n      id\n      name\n    }\n  }\n}",
            "variables": {}
        }
    }

    def __init__(self):
        self.session = requests.Session()

    def fetch_data(self, data, user_uuid):
        self.headers["Referer"] = "http://mundo-minecraft.com:3000/player/" + user_uuid
        response = self.session.post("http://mundo-minecraft.com:3000/graphql", headers=self.headers, timeout=60, allow_redirects=False, data=json.dumps(data))
        response.raise_for_status()
        return response.json()

    def create_ban(self, source, url, reason, date, expires):
        return {
            'source': source,
            'url': url,
            'reason': translate(reason) if get_language(reason) != 'en' else reason,
            'date': date,
            'expires': "Permanent" if expires == 0 else expires
        }
    def parse_website_html(self, response_json, url, type):
        bans = []

        if response_json['data'] is None:
            return bans

        response_json_data = response_json['data']

        if response_json_data.get(type) and len(response_json_data[type]) > 0:
            if type == BanType.PLAYER_BANS.value:
                _response_json_data = response_json_data[type][0]
                ban = self.create_ban('mundominecraft', url, _response_json_data['reason'], _response_json_data['created'], _response_json_data['expires'])
                bans.append(ban)

            elif type == BanType.LIST_PLAYER_PUNISHMENT_RECORDS.value:
                _response_json_data = response_json_data[type]['records']
                for record in _response_json_data:
                    ban = self.create_ban('mundominecraft', url, record['reason'], record['created'], record['expired'])
                    bans.append(ban)
            else:
                raise Exception("Unknown type: " + type)

        return bans

    def get_query_variables(self, type, user_uuid):
        if type == 'listPlayerPunishmentRecords':
            return {
                "activePage": 1,
                "limit": 20,
                "offset": 0,
                "serverId": "4044b44c",
                "player": user_uuid,
                "type": "PlayerBanRecord"
            }
        elif type == 'playerBans':
            return {"id": user_uuid}
        else:
            raise Exception("Unknown type: " + type)

    def get_response(self, url, type):
        user_uuid = url.split("/player/")[1]
        data = self.queries[type].copy()  # create a copy of the query
        data["variables"] = self.get_query_variables(type, user_uuid)  # get the variables for the query
        return self.fetch_data(data, user_uuid)

    def handle_request(self, url):
        try:
            response_text_player_query = self.get_response(url, type="playerBans")
            response_text_list_punishment_record = self.get_response(url, type="listPlayerPunishmentRecords")

            _bans = []
            if response_text_player_query is not None:
                _bans.extend(self.parse_website_html(response_text_player_query, url, type="playerBans"))
            if response_text_list_punishment_record is not None:
                _bans.extend(self.parse_website_html(response_text_list_punishment_record, url, type="listPlayerPunishmentRecords"))
            return _bans
        except requests.exceptions.RequestException as e:
            tqdm.write(str(e) + url)
            return None
        except KeyError as e:
            raise KeyError("Error: " + str(e)) from e