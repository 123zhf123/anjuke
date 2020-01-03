# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Anjuke_fy_rent2(scrapy.Item):
    tag = scrapy.Field()
    city = scrapy.Field()
    house_id = scrapy.Field()
    name = scrapy.Field()
    rent_price = scrapy.Field()
    community_price = scrapy.Field()
    district_price = scrapy.Field()
    release_time = scrapy.Field()
    district_name = scrapy.Field()
    community_name = scrapy.Field()
    house_type = scrapy.Field()
    house_area = scrapy.Field()
    block_name = scrapy.Field()
    addr = scrapy.Field()
    type_ = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    create_time = scrapy.Field()
    link = scrapy.Field()
    origin_price_data = scrapy.Field()


class Anjuke_xq_sale(scrapy.Item):
    tag = scrapy.Field()
    city = scrapy.Field()
    district_name = scrapy.Field()
    community_name = scrapy.Field()
    price = scrapy.Field()
    addr = scrapy.Field()
    type_ = scrapy.Field()
    build_time = scrapy.Field()
    developer = scrapy.Field()
    shangquan = scrapy.Field()
    price_3year = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    page = scrapy.Field()
    block_name = scrapy.Field()
