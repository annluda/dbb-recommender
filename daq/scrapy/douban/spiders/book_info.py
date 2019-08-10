# -*- coding: utf-8 -*-
import scrapy
import random
import string
from douban.items import BookInfo
from .db_query import query
import sys
import re


if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class BookInfoSpider(scrapy.Spider):
    name = "book_info"

    def start_requests(self):
        sql = 'SELECT id FROM `books` WHERE `name` IS NULL'
        ids = query(sql)
        urls = ('https://book.douban.com/subject/%s/' % i[0] for i in ids)

        for url in urls:
            cookies = {'bid': ''.join(random.sample(string.ascii_letters + string.digits, 11))}
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        book = BookInfo()
        for field in book.fields.keys():
            book[field] = None
        book['id'] = response.url[32:-1]

        if response.status == 404:
            book['name'] = '404'
            return book

        title = response.xpath('//title/text()').get()
        tags = response.xpath('//a[@class="  tag"]/text()').getall()
        score = response.xpath('//strong[@property="v:average"]/text()').get()
        votes = response.xpath('//span[@property="v:votes"]/text()').get()
        summary = response.xpath('id("link-report")//div[@class="intro"]/p/text()').getall()
        author_intro = response.xpath('//div[@class="indent "]//div[@class="intro"]/p/text()').getall()
        rec_ebook = response.xpath('id("rec-ebook-section")//div[@class="title"]/a/text()').getall()
        rec_book = response.xpath('id("db-rec-section")//dd/a/text()').getall()

        if title:
            book['name'] = title.replace(u' (豆瓣)', '')
        else:
            return
        if tags:
            book['tags'] = '/'.join(tags)
        if score:
            if not score.isspace():
                book['score'] = float(score)
        if votes:
            book['votes'] = int(votes)
        else:
            book['votes'] = 0
        if summary:
            book['summary'] = '\n'.join(summary)
        if author_intro:
            book['author_intro'] = '\n'.join(author_intro)
        if rec_ebook:
            book['rec_ebook'] = '/'.join(rec_ebook)
        if rec_book:
            book['rec_book'] = '/'.join([x.strip() for x in rec_book])

        info_text = response.xpath('id("info")//text()').getall()
        info_list = [s.strip().strip(':') for s in info_text if s.strip().strip(':') != '']
        info = dict(zip(info_list[0::2], info_list[1::2]))
        book['author'] = info.get(u'作者')
        book['translator'] = info.get(u'译者')
        book['series'] = info.get(u'丛书')
        book['publisher'] = info.get(u'出版社')
        book['publish_year'] = info.get(u'出版年')
        book['pages'] = info.get(u'页数')
        book['price'] = info.get(u'定价')
        book['binding'] = info.get(u'装帧')
        book['isbn'] = info.get(u'ISBN')

        if book['price']:
            price = re.findall(r'\d+\.?\d*', book['price'])
            if price:
                book['price'] = price[0]

        return book
