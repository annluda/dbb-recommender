# -*- coding: utf-8 -*-
import scrapy
from douban.items import BookInfo


class BookInfoSpider(scrapy.Spider):
    name = "book_info"

    def start_requests(self):
        # todo 从mysql取id 拼接URL
        urls = [
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        book = BookInfo()
        for field in book.fields.keys():
            book[field] = None
        book['id'] = ''
        book['name'] = ''
        book['sub_name'] = ''
        book['alt_name'] = ''
        book['summary'] = ''
        book['authors'] = ''
        book['author_intro'] = ''
        book['translators'] = ''
        book['series'] = ''
        book['publisher'] = ''
        book['publish_date'] = ''
        book['pages'] = ''
        book['price'] = ''
        book['binding'] = ''
        book['isbn'] = ''
        book['score'] = ''
        book['votes'] = ''
        book['tags'] = ''

        return book
