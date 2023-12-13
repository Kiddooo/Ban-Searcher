import scrapy

class BanItem(scrapy.Item):
    """
    BanItem represents a ban record scraped from a website.

    Fields:
        source: The source website of the ban record.
        url: The URL of the ban record.
        reason: The reason for the ban.
        date: The date when the ban was issued.
        expires: The date when the ban expires.
    """
    source = scrapy.Field()
    url = scrapy.Field()
    reason = scrapy.Field()
    date = scrapy.Field()
    expires = scrapy.Field()

    def to_json(self) -> dict:
        """
        Convert the BanItem to a JSON serializable dictionary.

        Returns:
            A dictionary with the same fields as the BanItem.
        """
        return {
            'source': self['source'],
            'url': self['url'],
            'reason': self['reason'],
            'date': self['date'],
            'expires': self['expires']
        }