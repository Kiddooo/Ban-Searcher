from typing import ClassVar, Optional
from uuid import UUID

import requests
from pydantic import BaseModel, HttpUrl, validator
from requests.exceptions import RequestException


class PlayerValidationError(Exception):
    """
    Custom exception class for handling validation errors in the Player class.
    """

    pass


class Player(BaseModel):
    SESSION_API_URL: ClassVar[HttpUrl] = (
        "https://sessionserver.mojang.com/session/minecraft/profile/"
    )
    API_URL: ClassVar[HttpUrl] = "https://api.mojang.com/users/profiles/minecraft/"
    username: Optional[str] = None
    uuid: Optional[str] = None
    uuid_dash: Optional[str] = None

    def fetch_username_from_uuid(self):
        """
        Fetches the username of a player from their UUID by making a request to the Mojang session server API.

        Inputs:
        - self: The instance of the Player class.

        Flow:
        1. Check if the `uuid` attribute of the Player instance is not empty.
        2. If the `uuid` attribute is not empty, construct the API URL by appending the `uuid` to the `SESSION_API_URL` class variable.
        3. Make a GET request to the constructed URL using a session object from the `requests` library.
        4. If the response status code is 200 (indicating a successful request), parse the response JSON and check if it contains the key "name".
        5. If the key "name" is present in the response JSON, assign its value to the `username` attribute of the Player instance.

        Outputs:
        - None. The method updates the `username` attribute of the Player instance with the fetched username value.
        """
        if self.uuid:
            url = f"{self.SESSION_API_URL}{self.uuid}"
            try:
                with requests.Session() as session:
                    response = session.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if "name" in data:
                            self.username = data["name"]
            except RequestException:
                pass

    def fetch_uuid_from_username(self):
        """
        Fetches the UUID of a player from their username by making a request to the Mojang API.

        Inputs:
        - self: The instance of the Player class.

        Flow:
        1. Check if the `username` attribute of the Player instance is not empty.
        2. If the `username` attribute is not empty, construct the API URL by appending the `username` to the `API_URL` class variable.
        3. Make a GET request to the constructed URL using a session object from the `requests` library.
        4. If the response status code is 200 (indicating a successful request), parse the response JSON and check if it contains the key "id".
        5. If the key "id" is present in the response JSON, assign its value to the `uuid` attribute of the Player instance.

        Outputs:
        - None. The method updates the `uuid` attribute of the Player instance with the fetched UUID value.
        """
        if self.username:
            url = f"{self.API_URL}{self.username}"
            try:
                with requests.Session() as session:
                    response = session.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if "id" in data:
                            self.uuid = data["id"]
            except RequestException:
                pass

    def convert_uuid_to_uuid_dash(self):
        """
        Converts the UUID attribute to its canonical form with dashes.

        Example Usage:
        player = Player()
        player.uuid = "1234567890abcdef1234567890abcdef"
        player.convert_uuid_to_uuid_dash()
        print(player.uuid_dash)  # Output: "12345678-90ab-cdef-1234-567890abcdef"

        Inputs:
        - self (implicit): The instance of the Player class.

        Flow:
        1. Check if the uuid attribute is not empty.
        2. If the uuid attribute is not empty, try to convert it to its canonical form with dashes using the UUID class.
        3. If the conversion is successful, assign the converted UUID to the uuid_dash attribute.
        4. If the conversion fails due to an invalid UUID format, catch the ValueError exception and do nothing.

        Outputs:
        - None. The method updates the uuid_dash attribute of the Player instance.
        """
        if self.uuid:
            try:
                # Convert the UUID to its canonical form (with dashes)
                uuid_with_dashes = str(UUID(self.uuid))
                self.uuid_dash = uuid_with_dashes
            except ValueError:
                # Handle the exception if the UUID is not in the correct format
                pass

    @validator("uuid", pre=True, always=True)
    def ensure_uuid(cls, value, values):
        """
        Ensures that the uuid attribute of the Player class is populated.

        If the uuid attribute is not set and the username attribute is set, the method makes a request to the Mojang API to fetch the UUID corresponding to the username.

        Args:
            cls: The class object.
            value: The current value of the uuid attribute.
            values: A dictionary containing the current values of all attributes.

        Returns:
            The updated value of the uuid attribute, which is the UUID fetched from the Mojang API or the current value if it was already set.
        """
        if not value and values.get("username"):
            url = f'{cls.API_URL}{values["username"]}'
            try:
                with requests.Session() as session:
                    response = session.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if "id" in data:
                            return data["id"]
            except RequestException:
                pass
        return value

    @validator("uuid_dash", pre=True, always=True)
    def ensure_uuid_dash(cls, value, values):
        """
        Ensures that the `uuid_dash` attribute is populated by converting the `uuid` attribute to its canonical form with dashes.

        :param cls: The class object.
        :param value: The current value of the `uuid_dash` attribute.
        :param values: A dictionary containing the current values of all attributes.
        :return: The updated value of the `uuid_dash` attribute, which is the canonical form of the `uuid` attribute with dashes.
        :raises ValueError: If the conversion fails due to an invalid UUID format.
        """
        if not value and values.get("uuid"):
            # Convert the UUID to its canonical form (with dashes)
            try:
                uuid_with_dashes = str(UUID(values["uuid"]))
                return uuid_with_dashes
            except ValueError as e:
                raise ValueError("Invalid UUID format") from e
        return value

    @validator("username", pre=True, always=True)
    def ensure_username(cls, value, values):
        """
        Ensures that the `username` attribute is populated by making a request to the Mojang API if it is not already set.

        :param cls: The class object.
        :param value: The current value of the `username` attribute.
        :param values: A dictionary containing the current values of all attributes.
        :return: The updated value of the `username` attribute.
        """
        if not value and values.get("uuid"):
            # Instead of creating a new instance, call the API directly
            url = f'{cls.SESSION_API_URL}{values["uuid"]}'
            try:
                with requests.Session() as session:
                    response = session.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if "name" in data:
                            return data["name"]
            except RequestException:
                pass
        return value

    def ensure_all_attributes(self):
        if not self.username and self.uuid:
            self.fetch_username_from_uuid()
        if not self.uuid and self.username:
            self.fetch_uuid_from_username()
        if not self.uuid_dash and self.uuid:
            self.convert_uuid_to_uuid_dash()
