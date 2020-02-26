# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeBrandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Province= scrapy.Field(),
    ProvinceId= scrapy.Field(),
    ProvincePinyin= scrapy.Field(),
    City= scrapy.Field(),
    CityId= scrapy.Field(),
    CityPinyin= scrapy.Field(),
    OldCityId= scrapy.Field(),

class AutohomeAreaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AutohomeDealerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AutohomeSeriesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AutohomeSpecItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass