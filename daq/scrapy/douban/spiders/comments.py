# -*- coding: utf-8 -*-
import scrapy
import random
import string
from douban.items import Comment
from .db_query import query
import sys


if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class CommentsSpider(scrapy.Spider):
    name = 'comment'

    def start_requests(self):
        sql = 'SELECT a.id FROM books a LEFT JOIN comments b ON a.id = b.book_id ' \
              'WHERE a.votes > 100 AND b.book_id IS NULL'
        ids = query(sql)
        urls = ('https://book.douban.com/subject/%s/comments/hot' % i[0] for i in set(ids))

        for url in urls:
            cookies = {'bid': ''.join(random.sample(string.ascii_letters + string.digits, 11))}
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def parse(self, response):

        comments = response.xpath('id("comments")/ul//li//p/span/text()').getall()

        for c in comments:
            comment = Comment()
            comment['book_id'] = response.url[32:39]
            comment['comment'] = c
            yield comment
