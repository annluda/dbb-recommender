# -*- coding: utf-8 -*-
import scrapy


class BookInfo(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    summary = scrapy.Field()
    author = scrapy.Field()
    author_intro = scrapy.Field()
    translator = scrapy.Field()
    series = scrapy.Field()
    publisher = scrapy.Field()
    publish_year = scrapy.Field()
    pages = scrapy.Field()
    price = scrapy.Field()
    binding = scrapy.Field()
    isbn = scrapy.Field()
    score = scrapy.Field()
    votes = scrapy.Field()
    tags = scrapy.Field()
    rec_ebook = scrapy.Field()
    rec_book = scrapy.Field()


class Comment(scrapy.Item):
    book_id = scrapy.Field()
    comment = scrapy.Field()
