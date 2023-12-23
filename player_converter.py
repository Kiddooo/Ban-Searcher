import requests
import re
import traceback

class PlayerConverter:
    def __init__(self, input_value, input_type):
        self.input_value = input_value
        self.input_type = input_type

    def convert(self):
        if self.input_type == 'Username':
            username = self.input_value
            uuid = self.username_to_uuid(username)
            uuid_dash = self.uuid_to_uuid_dash(uuid)
        elif self.input_type == 'UUID':
            uuid = self.input_value
            username = self.uuid_to_username(uuid)
            uuid_dash = self.uuid_to_uuid_dash(uuid)
        else:  # UUID with dashes
            uuid_dash = self.input_value
            uuid = self.uuid_dash_to_uuid(uuid_dash)
            username = self.uuid_to_username(uuid)

        return username, uuid, uuid_dash

    @staticmethod
    def uuid_to_username(uuid):
        url = ("https://sessionserver.mojang.com/session/minecraft/profile/{}").format(uuid)
        try:
            response = requests.get(url, timeout=5).json()
            return response["name"]
        except KeyError:
            print("Username not found for UUID.")

    @staticmethod
    def username_to_uuid(username):
        api_url = "https://api.mojang.com/users/profiles/minecraft/"
        try:
            response = requests.get(f"{api_url}{username}", timeout=5)
            response_json = response.json()
            return response_json["id"]
        except KeyError:
            return traceback.format_exc()

    @staticmethod
    def uuid_to_uuid_dash(UUID):
        matcher = re.search(
            "([a-f0-9]{8})([a-f0-9]{4})([0-5][0-9a-f]{3})([089ab][0-9a-f]{3})([0-9a-f]{12})",
            UUID,
        )
        return f"{matcher.group(1)}-{matcher.group(2)}-{matcher.group(3)}-{matcher.group(4)}-{matcher.group(5)}"

    @staticmethod
    def uuid_dash_to_uuid(uuid_dash):
        return uuid_dash.replace("-", "")