import scrapy


class BanItem(scrapy.Item):
    """
    A class representing a ban.

    Attributes:
        source (str): The source of the ban.
        url (str): The URL of the banned entity.
        reason (str): The reason for the ban.
        date (str): The date when the ban was issued.
        expires (str): The date when the ban expires.
    """

    source = scrapy.Field()
    url = scrapy.Field()
    reason = scrapy.Field()
    date = scrapy.Field()
    expires = scrapy.Field()

    def to_json(self) -> dict:
        """
        Convert the BanItem object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the BanItem object.
        """
        return {
            "source": self["source"].capitalize(),
            "url": self["url"],
            "reason": self["reason"],
            "date": self["date"],
            "expires": self["expires"],
        }
