import scrapy


class BanItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    reason = scrapy.Field()
    date = scrapy.Field()
    expires = scrapy.Field()

    def to_json(self) -> dict:
        return {
            "source": self["source"].capitalize(),
            "url": self["url"],
            "reason": self["reason"],
            "date": self["date"],
            "expires": self["expires"],
        }
