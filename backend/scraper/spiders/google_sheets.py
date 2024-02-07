import re
from typing import Generator, List, Union

import scrapy
from colorama import Fore, Style
from google.oauth2 import service_account
from googleapiclient.discovery import build
from twisted.internet.threads import deferToThread

from backend.utils import calculate_timestamp, logger, parse_date
from scraper.items import BanItem


class GoogleSheetsSpider(scrapy.Spider):
    name = "GoogleSheetsSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the GoogleSheetsSpider object.

        Args:
            username (str): The username of the player.
            player_uuid (str): The UUID of the player.
            player_uuid_dash (str): The UUID of the player with dashes.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        if not all([username, player_uuid, player_uuid_dash]):
            raise ValueError("Invalid parameters")

        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash

    def start_requests(self):
        """
        Generator function that yields a scrapy.Request object to initiate the spider.
        """
        yield scrapy.Request(
            url="https://example.com", callback=self.parse, dont_filter=True
        )

    def parse(self, response):
        # Initiate the processing by deferring to a thread
        return deferToThread(self.read_google_sheets)

    def _parse_date(self, date_string: str) -> Union[int, str]:
        """
        Parse a date string and return the corresponding timestamp.

        Args:
            date_string (str): The date string to be parsed.

        Returns:
            Union[int, str]: The timestamp of the parsed date string. If the parsing fails or the year is not present, it returns "N/A".
        """
        # Check if the date string contains a year
        if re.search(r"\b\d{4}\b", date_string):
            # Year is present, so try to parse the date string into a date object
            parsed_date = parse_date(date_string, settings={})
            if parsed_date:
                # If parsing was successful, return the timestamp
                return calculate_timestamp(parsed_date)
        # If year is not present or parsing failed, return "N/A"
        return "N/A"

    def read_google_sheets(self) -> Generator[BanItem, None, None]:
        """
        Reads data from two ranges in a Google Sheets document using the Google Sheets API.
        Retrieves the values from the "Universal Ban List" range and the "Previously Banned" range,
        and yields `BanItem` objects for each row that matches the player's UUID.
        """
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        SPREADSHEET_ID = "1VdyBZs4B-qoA8-IijPvbRUVBLfOuU9I5fV_PhuOWJao"
        RANGE_NAME = "Universal Ban List"
        RANGE_NAME_PREV = "Previously Banned"
        creds = service_account.Credentials.from_service_account_file(
            "credentials.json", scopes=SCOPES
        )
        service = build("sheets", "v4", credentials=creds)

        logger.info(
            f"{Fore.YELLOW}{self.name} | Started Scraping: {SPREADSHEET_ID}{Style.RESET_ALL}"
        )

        def create_ban_item(row: List[str], source: str, url: str) -> BanItem:
            return BanItem(
                {
                    "source": source,
                    "url": url,
                    "reason": row[2],
                    "date": self._parse_date(row[3]),
                    "expires": "Permanent"
                    if row[4] == "Permanent"
                    else self._parse_date(row[5]),
                }
            )

        def yield_ban_items(
            values: List[List[str]], source: str, url: str
        ) -> Generator[BanItem, None, None]:
            for row in values:
                if row[1] == self.player_uuid_dash:
                    yield create_ban_item(row, source, url)

        # Read the first range "Universal Ban List"
        sheet = service.spreadsheets()
        ubl = (
            sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        )
        ubl_values = ubl.get("values", [])
        yield from yield_ban_items(
            ubl_values,
            "UHC Universal Ban List",
            f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0",
        )

        # Read the second range "Previously Banned"
        ubl_prev = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_PREV)
            .execute()
        )
        ubl_prev_values = ubl_prev.get("values", [])
        yield from yield_ban_items(
            ubl_prev_values,
            "UHC Universal Ban List - Previously Banned",
            f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=3",
        )
