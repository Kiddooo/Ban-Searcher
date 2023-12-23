import re
import dateparser
import scrapy
from twisted.internet.threads import deferToThread
from google.oauth2 import service_account
from googleapiclient.discovery import build

from banlist_project.items import BanItem

class GoogleSheetsSpider(scrapy.Spider):
    name = 'google_sheets_spider'
    
    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(GoogleSheetsSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash


    def start_requests(self):
        yield scrapy.Request(
            url='https://example.com',  # Dummy request to initiate the spider
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        # Initiate the processing by deferring to a thread
        return deferToThread(self.read_google_sheets)
    
    def parse_date(self, date_string):
        # Check if the date string contains a year
        if re.search(r'\b\d{4}\b', date_string):
            try:
                # Year is present, so try to parse the date string into a date object
                parsed_date = dateparser.parse(date_string)
                if parsed_date:
                    # If parsing was successful, return the timestamp
                    return int(parsed_date.timestamp())
            except Exception as e:
                # Log the exception for debugging purposes
                self.logger.error(f"Exception occurred: {e}")
        # If year is not present or parsing failed, return "N/A"
        return "N/A"

    def read_google_sheets(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        SPREADSHEET_ID = '1VdyBZs4B-qoA8-IijPvbRUVBLfOuU9I5fV_PhuOWJao'
        RANGE_NAME = 'Universal Ban List'  # Replace with your actual range name
        RANGE_NAME_PREV = 'Previously Banned'  # Replace with your actual range name
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        # Read the first range "Universal Ban List"
        sheet = service.spreadsheets()
        ubl = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        ubl_values = ubl.get('values', [])

        # Yield data from the "Universal Ban List"
        for row in ubl_values:
            if row[1] == self.player_uuid_dash:
                yield BanItem({
                    'source': "UHC Universal Ban List",
                    'url': f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0',
                    'reason': row[2],
                    'date': self.parse_date(row[3]),
                    'expires': 'Permanent' if row[4] == 'Permanent' else int(dateparser.parse(row[5]).timestamp())
                })

        # Read the second range "Previously Banned"
        ubl_prev = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_PREV).execute()
        ubl_prev_values = ubl_prev.get('values', [])

        # Yield data from the "Previously Banned"
        for row in ubl_prev_values:
            if row[1] == self.player_uuid_dash:
                yield BanItem({
                    'source': "UHC Universal Ban List - Previously Banned",
                    'url': f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=3',
                    'reason': row[2],
                    'date': self.parse_date(row[3]),
                    'expires': 'Permanent' if row[4] == 'Permanent' else int(dateparser.parse(row[5]).timestamp())
                })