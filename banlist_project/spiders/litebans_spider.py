import dateparser
import scrapy
from banlist_project.items import BanItem
from bs4 import BeautifulSoup
import urllib.parse
import re
import tldextract
from utils import get_language, translate, logger

class LiteBansSpider(scrapy.Spider):
    name = 'LiteBansSpider'

    def __init__(self, username, player_uuid, player_uuid_dash, *args, **kwargs):
        super(LiteBansSpider, self).__init__(*args, **kwargs)
        self.player_username = username
        self.player_uuid = player_uuid
        self.player_uuid_dash = player_uuid_dash
        self.pattern = re.compile(r".*(\bNon è mai entrato\b)|(\bNo ha entrado al servidor\b)|(\bnot found in database\b)|(\bhas not joined before\b)|(\bEventyrCraftIngen Straffe Fundet\b)|(\bNo se encontraron sanciones.\b)|(\bno existe\b).*", flags=re.IGNORECASE)
    def start_requests(self):
        urls = [
            "http://diemeesmcbans.nl/bans/history.php?uuid=",
            "http://prestigebans.xyz/history.php?uuid=",
            "http://www.dodedge.com/bans/history.php?uuid=",
            "http://www.pokerevolution.es/bans/history.php?uuid=",
            "https://advanciuspunishments.website/history.php?uuid=",
            "https://alttd.com/bans/history?uuid=",
            "https://atomicnetwork.eu/bans/history.php?uuid=",
            "https://ban.laborcraft.net/history.php?uuid=",
            "https://banlog.mythictales.it/history.php?uuid=",
            "https://bans.dogecraft.net/history.php?uuid=",
            "https://bans.dragonstone.pw/history.php?uuid=",
            "https://bans.g4meworld.net/history.php?uuid=",
            "https://bans.gp-mc.net/history.php?uuid=",
            "https://bans.horizonsend.net/history.php?uuid=",
            "https://bans.hublolland.dk/history.php?uuid=",
            "https://bans.kiwismp.fun/history.php?uuid=",
            "https://bans.neocubest.com/history?uuid=",
            "https://bans.pixelgaming.co/history.php?uuid=",
            "https://bans.purityvanilla.com/history.php?uuid=",
            "https://bans.renatusnetwork.com/history.php?uuid=",
            "https://bans.secure-heaven.com/history.php?uuid=",
            "https://bans.shadowraptor.net/history.php?uuid=",
            "https://bans.siriusmc.net/history.php?uuid=",
            "https://bans.skykingdoms.net/history.php?uuid=",
            "https://bans.skyversecraft.eu/history.php?uuid=",
            "https://bans.sootmc.net/history.php?uuid="
            "https://bans.truesmp.org/history.php?uuid=",
            "https://bans.unitedfactions.net/history.php?uuid=",
            "https://bans.valatic.net/history.php?uuid=",
            "https://bans.yesssirbox.xyz/history.php?uuid=",
            "https://bluecraft.dk/bans/history.php?uuid=",
            "https://bridger.land/bans/history.php?uuid=",
            "https://build.mcmiddleearth.com/bans/history.php?uuid=",
            "https://corn.gg/bans/history.php?uuid=",
            "https://dankprison.com/bans/history.php?uuid=",
            "https://differentcraft.net/bans/history.php?uuid=",
            "https://hearthcraft.net/bans/history.php?uuid=",
            "https://hydrapvp.it/bans/history.php?uuid=",
            "https://infracciones.acropolis-mc.com/history.php?uuid=",
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
            "https://opblocks.com/bans/history.php?uuid=",
            "https://ottercraft.net/LiteBans/history.php?uuid=",
            "https://punishments.direskies.net/history.php?uuid=",
            "https://rankku.motimaa.net/history/",
            "https://siphonmc.com/bans/history/",
            "https://site.cynagen.xyz/bans/history.php?uuid=",
            "https://void-craft.net/history.php?uuid=",
            "https://wickedworlds.ca/bans/history.php?uuid=",
            "https://www.airidale.net/bans/history.php?uuid=",
            "https://www.hoobs.live/minecraft/bans/history.php?uuid=",
            "https://www.karmacraft.es/Sanciones/history.php?uuid=",
            "https://www.kingscraft.co.uk/bans/history.php?uuid=",
            "https://www.minelife.eu/bans/history.php?uuid=",
            "https://www.mooncraft.es/bans/history.php?uuid=",
            "https://www.myinstacraft.com/bans/history.php?uuid=",
            "https://www.paladia.net/history.php?uuid=",
            "https://www.roxbot.com/bans/history.php?uuid=",
            "https://www.staxified.net/litebans/history.php?uuid=",
            ]
        for url in urls:
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
            "https://www.pickaxemania.com/playerstatus/history.php?uuid="
        
        ]
        for url in urls2:
            url = url + self.player_uuid_dash
            if "saicopvp" in url:
                yield scrapy.Request(url, callback=self.parse, meta={'flare_solver': True})
            else:
                yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        
        if soup.find_all(string="No punishments found."):
            return

        if self.pattern.search(soup.text):
            return

        table = soup.find('table')
        if table is not None:
            header_row = table.find('tr')  # Adjust this as needed
            headers = [cell.text.strip().lower() for cell in header_row.find_all('th')]
            # Translate headers to standard keys
            headers = [self.translate_header('reason', header) or self.translate_header('date', header) or self.translate_header('expires', header) for header in headers]
            # Find the indices of the cells we're interested in
            reason_index = headers.index('reason')  # Adjust these as needed
            date_index = headers.index('date')
            expiry_index = headers.index('expires')

            
            for row in table.find_all('tr')[1:]: # Skip the header row
                columns = row.find_all('td')
                ban_type = columns[0].text.strip()
                if ban_type.lower() in ['ban', 'porttikielto']:
                    ban = self.generate_ban(columns, response.url, reason_index, date_index, expiry_index)
                    yield ban
                else:
                    continue
                                        

            # Find the div with pagination information
            page_info_div = soup.find('div', class_='litebans-pager-number')
            if not page_info_div:
                page_info_div = soup.find('div', style="text-align: center; font-size:15px;")
            if page_info_div:
                page_info_text = page_info_div.get_text()
                current_page, total_pages = map(int, re.findall(r'\d+', page_info_text))
                
                # Check if you're on the last page
                if current_page < total_pages:
                    next_page = soup.find("div", class_="litebans-pager litebans-pager-right litebans-pager-active")
                    if next_page and next_page.parent.name == 'a':  # Ensure it's an anchor tag for a valid URL
                        next_page_url = urllib.parse.urljoin(response.url, next_page.parent['href'])
                        if "saicopvp" in next_page_url:
                            yield scrapy.Request(next_page_url, callback=self.parse, meta={'flare_solver': True})
                        else: 
                            yield scrapy.Request(next_page_url, callback=self.parse)

    def generate_ban(self, columns, url, reason_index, date_index, expiry_index):
        ban_reason = columns[reason_index].text
        ban_date = columns[date_index].text
        ban_expiry = columns[expiry_index].text

        try:
            ban_expiry = ban_expiry.replace("klo", "").split(" (")[0].strip()
            if ban_expiry in ("Permanent Ban", "Permanentni", "Ban Permanente"):
                ban_expires = "Permanent"
            else:
                try:
                    ban_expires = int(dateparser.parse(ban_expiry).timestamp())
                except ValueError:
                    logger.error("Failed to parse ban expiry:", ban_expiry)
                    ban_expires = 'N/A'

            ban_date_text = ban_date.replace("klo", "").split(" (")[0].strip()
            try:
                ban_date = int(dateparser.parse(ban_date_text).timestamp())
            except ValueError:
                logger.error("Failed to parse ban date:", ban_date_text)
                ban_date = "N/A"

            ban_reason = ban_reason.encode("ascii", "ignore").decode()
            ban = BanItem({
                'source': tldextract.extract(url).domain,
                'url': url,
                'reason': translate(ban_reason) if get_language(ban_reason) != 'en' else ban_reason,
                'date': ban_date,
                'expires': ban_expires
            })

            return ban
        except Exception as e:
            raise Exception(f"Failed to generate ban: {e}") from e

    def translate_month(self, date_string):
        spanish_to_english = {
            'enero': 'January',
            'febrero': 'February',
            'marzo': 'March',
            'abril': 'April',
            'mayo': 'May',
            'junio': 'June',
            'julio': 'July',
            'agosto': 'August',
            'septiembre': 'September',
            'octubre': 'October',
            'noviembre': 'November',
            'diciembre': 'December'
        }
        for spanish, english in spanish_to_english.items():
            date_string = date_string.replace(spanish, english)
        return date_string

    def translate_header(self, type, header):
        header = header.lower()
        reason_translations = {
            'en': ['reason'],
            'es': ['motivo', 'razón'],   # Spanish
            'de': ['grund'],             # German
            'fi': ['syy'],               # Finnish
            'it': ['motivazione'],       # Italian
            'fr': ['raison'],            # French
            'pt': ['motivo', 'razão'],   # Portuguese
            'ru': ['причина'],          # Russian
            'ja': ['理由'],             # Japanese
            'zh': ['原因'],             # Chinese
            'ar': ['سبب'],              # Arabic
            'dk': ['grund']             # Danish
            # Add more translations as needed
        }
        date_translations = {
            'en': ['date', 'when', 'banned on'],
            'es': ['fecha'],  # Spanish
            'de': ['datum'],  # German
            'fi': ['päivämäärä'],  # Finnish
            'it': ['data'],  # Italian
            'fr': ['date'],  # French
            'pt': ['data'],  # Portuguese
            'ru': ['дата'],  # Russian
            'ja': ['日付'],  # Japanese
            'zh': ['日期'],  # Chinese
            'ar': ['تاريخ'],# Arabic
            'dk': ['dato']   # Danish
            # Add more translations as needed
        }
        expiry_translations = {
            'en': ['expires', 'banned until'],
            'es': ['expira'],  # Spanish
            'de': ['ablauf'],  # German
            'fi': ['vanhenee'],  # Finnish
            'it': ['scadenza'],  # Italian
            'fr': ['expire'],  # French
            'pt': ['expira'],  # Portuguese
            'ru': ['истекает'],  # Russian
            'ja': ['有効期限'],  # Japanese
            'zh': ['到期'],  # Chinese
            'ar': ['تنتهي'],# Arabic
            'dk': ['Udløber']   # Danish
            # Add more translations as needed
        }
        
        translations = {
            'reason': reason_translations,
            'date': date_translations,
            'expires': expiry_translations,
        }
        
        for key, value in translations.items():
            for _lang, terms in value.items():
                if header in terms:
                    return key
        
        return None