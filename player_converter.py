from pydantic import BaseModel, validator, HttpUrl
from typing import ClassVar, Optional
from uuid import UUID
import requests

class Player(BaseModel):
    SESSION_API_URL: ClassVar[HttpUrl] = 'https://sessionserver.mojang.com/session/minecraft/profile/'
    API_URL: ClassVar[HttpUrl] = 'https://api.mojang.com/users/profiles/minecraft/'
    username: Optional[str] = None
    uuid: Optional[str] = None
    uuid_dash: Optional[str] = None

    def fetch_username_from_uuid(self):
        if self.uuid:
            url = f'{self.SESSION_API_URL}{self.uuid}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.username = data['name']

    def fetch_uuid_from_username(self):
        if self.username:
            url = f'{self.API_URL}{self.username}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.uuid = data['id']

    def convert_uuid_to_uuid_dash(self):
        if self.uuid:
            try:
                # Convert the UUID to its canonical form (with dashes)
                uuid_with_dashes = str(UUID(self.uuid))
                self.uuid_dash = uuid_with_dashes
            except ValueError:
                # Handle the exception if the UUID is not in the correct format
                pass

    @validator('uuid', pre=True, always=True)
    def ensure_uuid(cls, value, values):
        if not value and values.get('username'):
            # Instead of creating a new instance, call the API directly
            url = f'{cls.API_URL}{values["username"]}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data['id']
        return value

    @validator('uuid_dash', pre=True, always=True)
    def ensure_uuid_dash(cls, value, values):
        if not value and values.get('uuid'):
            # Convert the UUID to its canonical form (with dashes)
            try:
                uuid_with_dashes = str(UUID(values['uuid']))
                return uuid_with_dashes
            except ValueError:
                pass
        return value

    @validator('username', pre=True, always=True)
    def ensure_username(cls, value, values):
        if not value and values.get('uuid'):
            # Instead of creating a new instance, call the API directly
            url = f'{cls.SESSION_API_URL}{values["uuid"]}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data['name']
        return value

    def ensure_all_attributes(self):
        if not self.username and self.uuid:
            self.fetch_username_from_uuid()
        if not self.uuid and self.username:
            self.fetch_uuid_from_username()
        if not self.uuid_dash and self.uuid:
            self.convert_uuid_to_uuid_dash()