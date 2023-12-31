import re
import urllib.parse
from typing import Optional

import scrapy
import tldextract
from bs4 import BeautifulSoup
from colorama import Fore, Style

from banlist_project.items import BanItem
from utils import calculate_timestamp, get_language, logger, parse_date, translate


class LiteBansSpider(scrapy.Spider):
    name = "LiteBansSpider"

    def __init__(
        self, username=None, player_uuid=None, player_uuid_dash=None, *args, **kwargs
    ):
        """
        Initialize the LiteBansSpider object.

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
        self.pattern = re.compile(
            r".*(\bNon è mai entrato\b)|(\bNo ha entrado al servidor\b)|(\bnot found in database\b)|(\bhas not joined before\b)|(\bEventyrCraftIngen Straffe Fundet\b)|(\bNo se encontraron sanciones.\b)|(\bno existe\b).*",
            flags=re.IGNORECASE,
        )

    def start_requests(self):
        """
        Generate a list of URLs and make HTTP requests to each URL using Scrapy.
        """
        urls = [
            "http://diemeesmcbans.nl/bans/history.php?uuid=",
            "http://prestigebans.xyz/history.php?uuid=",
            "http://www.dodedge.com/bans/history.php?uuid=",
            "http://www.pokerevolution.es/bans/history.php?uuid=",
            "https://advanciuspunishments.website/history.php?uuid=",
            "https://alttd.com/bans/history?uuid=",
            "https://atomicnetwork.eu/bans/history.php?uuid=",
            "https://ban.laborcraft.net/history.php?uuid=",
            # "https://banlog.mythictales.it/history.php?uuid=",
            "https://bans.dogecraft.net/history.php?uuid=",
            "https://bans.dragonstone.pw/history.php?uuid=",
            "https://bans.g4meworld.net/history.php?uuid=",
            "https://bans.gp-mc.net/history.php?uuid=",
            "https://bans.horizonsend.net/history.php?uuid=",
            "https://bans.hublolland.dk/history.php?uuid=",
            # "https://bans.kiwismp.fun/history.php?uuid=",
            "https://bans.neocubest.com/history?uuid=",
            "https://bans.pixelgaming.co/history.php?uuid=",
            "https://bans.purityvanilla.com/history.php?uuid=",
            "https://bans.renatusnetwork.com/history.php?uuid=",
            "https://bans.secure-heaven.com/history.php?uuid=",
            "https://bans.shadowraptor.net/history.php?uuid=",
            "https://bans.siriusmc.net/history.php?uuid=",
            "https://bans.skykingdoms.net/history.php?uuid=",
            "https://bans.skyversecraft.eu/history.php?uuid=",
            "https://bans.sootmc.net/history.php?uuid=",
            "https://bans.truesmp.org/history.php?uuid=",
            "https://bans.unitedfactions.net/history.php?uuid=",
            "https://bans.valatic.net/history.php?uuid=",
            # "https://bans.yesssirbox.xyz/history.php?uuid=",
            "https://bluecraft.dk/bans/history.php?uuid=",
            "https://bridger.land/bans/history.php?uuid=",
            "https://build.mcmiddleearth.com/bans/history.php?uuid=",
            "https://corn.gg/bans/history.php?uuid=",
            "https://dankprison.com/bans/history.php?uuid=",
            "https://differentcraft.net/bans/history.php?uuid=",
            "https://hearthcraft.net/bans/history.php?uuid=",
            "https://hydrapvp.it/bans/history.php?uuid=",
            # "https://infracciones.acropolis-mc.com/history.php?uuid=",
            "https://justleader.net/tresty/history/",
            "https://litebans.shiuki.eu.org/minersleague/punishments/history.php?uuid=",
            "https://lostgamers.eu/punishments/history.php?uuid=",
            "https://main.play.u3002.com/bans/history.php?uuid=",
            "https://medievalpvp.net/bans/history.php?uuid=",
            "https://minecochia.net/bans/history.php?uuid=",
            "https://minecraft-romania.ro/sanctiuni/history.php?uuid=",
            "https://minecraft.mgn.gg/bans/history.php?uuid=",
            "https://minedhype.com/bans/history.php?uuid=",
            "https://nd2.worldofkeralis.com/bans/history.php?uuid=",
            "https://ottercraft.net/LiteBans/history.php?uuid=",
            "https://punishments.direskies.net/history.php?uuid=",
            # "https://rankku.motimaa.net/history/",
            "https://siphonmc.com/bans/history/",
            "https://site.cynagen.xyz/bans/history.php?uuid=",
            "https://wickedworlds.ca/bans/history.php?uuid=",
            "https://www.airidale.net/bans/history.php?uuid=",
            "https://www.hoobs.live/minecraft/bans/history.php?uuid=",
            # "https://www.karmacraft.es/Sanciones/history.php?uuid=",
            "https://www.kingscraft.co.uk/bans/history.php?uuid=",
            "https://www.minelife.eu/bans/history.php?uuid=",
            "https://www.mooncraft.es/bans/history.php?uuid=",
            "https://www.myinstacraft.com/bans/history.php?uuid=",
            "https://www.paladia.net/history.php?uuid=",
            "https://www.roxbot.com/bans/history.php?uuid=",
            "https://www.staxified.net/litebans/history.php?uuid=",
        ]
        for url in urls:
            logger.info(
                f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
            )
            url = url + self.player_uuid
            yield scrapy.Request(url, callback=self.parse)

        urls2 = [
            "http://eventyrcraft.net/ban/history.php?uuid=",
            "https://minecraft.rtgame.co.uk/bans/history.php?uuid=",
            "https://saicopvp.com/bans/history.php?uuid=",
            "https://bans.astrocraft.org/history.php?uuid=",
            "https://punishments.baconetworks.com/history?uuid=",
            "https://play.hellominers.com/bans/history.php?uuid=",
            "https://nytro.co/bans/history.php?uuid=",
            "https://www.pickaxemania.com/playerstatus/history.php?uuid=",
            "https://opblocks.com/bans/history.php?uuid="
        ]
        for url in urls2:
            url = url + self.player_uuid_dash
            logger.info(
                f"{Fore.YELLOW}{self.name} | Started Scraping: {tldextract.extract(url).registered_domain}{Style.RESET_ALL}"
            )
            if "saicopvp" in url:
                yield scrapy.Request(
                    url, callback=self.parse, meta={"flare_solver": True}
                )
            else:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """
        Parse the response from a website and extract relevant information from the HTML table.
        Handles pagination by recursively calling itself to parse the next page.

        Args:
            response (scrapy.Response): The response object containing the HTML content of the website.

        Yields:
            dict: A ban object for each row in the table that corresponds to a ban or porttikielto.
        """
        soup = BeautifulSoup(response.text, "lxml")
        if soup.find_all(string="No punishments found."):
            return

        if self.pattern.search(soup.text):
            return

        table = soup.find("table")
        if table is not None:
            headers = self.extract_headers(table)
            reason_index, date_index, expiry_index = self.find_indices(headers)

            for row in table.find_all("tr")[1:]:  # Skip the header row
                columns = row.find_all("td")
                ban_type = columns[0].text.strip()
                if ban_type.lower() in ["ban", "porttikielto"]:
                    ban = self.generate_ban(
                        columns,
                        response.url,
                        reason_index,
                        date_index,
                        expiry_index,
                    )
                    yield ban

            page_info_div = soup.find("div", class_="litebans-pager-number")
            if not page_info_div:
                page_info_div = soup.select("div.container.containerCC div.col-lg-12 div div")

            if page_info_div:
                current_page, total_pages = self.extract_pagination_info(page_info_div)

                if current_page < total_pages:
                    next_page_url = self.find_next_page_url(response.url, soup)
                    if next_page_url:
                        if 'saicopvp' in next_page_url:
                            yield scrapy.Request(next_page_url, callback=self.parse, meta={'flare_solver': True})
                        else:
                            yield scrapy.Request(next_page_url, callback=self.parse)


    def extract_headers(self, table):
        """
        Extract the headers from the table and convert them to lowercase.

        Args:
            table (bs4.element.Tag): The HTML table element.

        Returns:
            list: The lowercase headers.
        """
        header_row = table.find("tr")
        headers = [cell.text.strip().lower() for cell in header_row.find_all("th")]
        return headers

    def find_indices(self, headers):
        """
        Find the indices of the cells corresponding to the reason, date, and expiry columns.

        Args:
            headers (list): The lowercase headers.

        Returns:
            tuple: The indices of the reason, date, and expiry columns.
        """
        translated_headers = [
            self.translate_header("reason", header)
            or self.translate_header("date", header)
            or self.translate_header("expires", header)
            for header in headers
        ]

        # Find the indices of the cells we're interested in
        reason_index = (
            translated_headers.index("reason")
            if "reason" in translated_headers
            else None
        )
        date_index = (
            translated_headers.index("date") if "date" in translated_headers else None
        )
        expiry_index = (
            translated_headers.index("expires")
            if "expires" in translated_headers
            else None
        )

        return reason_index, date_index, expiry_index

    def generate_ban(self, columns, url, reason_index, date_index, expiry_index):
        """
        Generate a ban object using the columns.

        Args:
            columns (list): The columns of a row in the table.
            url (str): The URL of the website.
            reason_index (int): The index of the reason column.
            date_index (int): The index of the date column.
            expiry_index (int): The index of the expiry column.

        Returns:
            dict: The ban object.
        """
        reason = columns[reason_index].text.strip()
        return BanItem(
            {
                "source": tldextract.extract(url).domain,
                "reason": translate(reason) if get_language(reason) != "en" else reason,
                "date": calculate_timestamp(
                    parse_date(columns[date_index].text.strip(), settings={})
                ),
                "expires": calculate_timestamp(
                    parse_date(columns[expiry_index].text.strip(), settings={})
                ),
                "url": url,
            }
        )

    def extract_pagination_info(self, page_info_div):
        """
        Extract the current page number and total number of pages from the pagination information.

        Args:
            page_info_div (bs4.element.Tag): The div element containing the pagination information.

        Returns:
            tuple: The current page number and total number of pages.
        """
        page_info_text = page_info_div.get_text()
        current_page, total_pages = map(int, re.findall(r"\d+", page_info_text))
        return current_page, total_pages

    def find_next_page_url(self, current_url, soup):
        """
        Find the URL of the next page.

        Args:
            current_url (str): The URL of the current page.
            soup (BeautifulSoup): The BeautifulSoup object of the current page.

        Returns:
            str: The URL of the next page, or None if not found.
        """
        next_page = soup.find(
            "div",
            class_="litebans-pager litebans-pager-right litebans-pager-active",
        )
        if next_page and next_page.parent.name == "a":
            next_page_url = urllib.parse.urljoin(current_url, next_page.parent["href"])
            return next_page_url

    def translate_header(self, type: str, header: str) -> Optional[str]:
        """
        Translates the header names in different languages.

        Args:
            type (str): The type of header to translate ('reason', 'date', 'expires').
            header (str): The header name to be translated.

        Returns:
            str: The translated header type or None if no translation is found.
        """
        header = header.lower()

        translations = {
            "reason": {
                "en": ["reason"],
                "es": ["motivo", "razón"],
                "de": ["grund"],
                "fi": ["syy"],
                "it": ["motivazione"],
                "fr": ["raison"],
                "pt": ["motivo", "razão"],
                "ru": ["причина"],
                "ja": ["理由"],
                "zh": ["原因"],
                "ar": ["سبب"],
                "dk": ["grund"],
            },
            "date": {
                "en": ["date", "when", "banned on"],
                "es": ["fecha"],
                "de": ["datum"],
                "fi": ["päivämäärä"],
                "it": ["data"],
                "fr": ["date"],
                "pt": ["data"],
                "ru": ["дата"],
                "ja": ["日付"],
                "zh": ["日期"],
                "ar": ["تاريخ"],
                "dk": ["dato"],
            },
            "expires": {
                "en": ["expires", "banned until"],
                "es": ["expira"],
                "de": ["ablauf"],
                "fi": ["vanhenee"],
                "it": ["scadenza"],
                "fr": ["expire"],
                "pt": ["expira"],
                "ru": ["истекает"],
                "ja": ["有効期限"],
                "zh": ["到期"],
                "ar": ["تنتهي"],
                "dk": ["udløber"],
            },
        }

        for key, value in translations.items():
            for _lang, terms in value.items():
                if header in terms:
                    return key

        return None
