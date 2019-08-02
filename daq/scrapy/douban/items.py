# -*- coding: utf-8 -*-
import scrapy


class BookInfo(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    sub_name = scrapy.Field()
    alt_name = scrapy.Field()
    summary = scrapy.Field()
    authors = scrapy.Field()
    author_intro = scrapy.Field()
    translators = scrapy.Field()
    series = scrapy.Field()
    publisher = scrapy.Field()
    publish_date = scrapy.Field()
    pages = scrapy.Field()
    price = scrapy.Field()
    binding = scrapy.Field()
    isbn = scrapy.Field()
    score = scrapy.Field()
    votes = scrapy.Field()
    tags = scrapy.Field()
