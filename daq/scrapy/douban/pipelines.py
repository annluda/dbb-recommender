# -*- coding: utf-8 -*-
import pymysql
from douban.items import BookInfo


class MysqlPipeline(object):

    def __init__(self, settings):
        self.mysql_host = settings.get('MYSQL_HOST')
        self.mysql_port = settings.get('MYSQL_PORT', 3306)
        self.mysql_user = settings.get('MYSQL_USER')
        self.mysql_passwd = settings.get('MYSQL_PASSWD')
        self.mysql_db = settings.get('MYSQL_DB')
        self.mysql_charset = settings.get('MYSQL_CHARSET', 'utf8mb4')
        self.items = []
        self._sql()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def open_spider(self, spider):
        self.spider = spider
        self.conn = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            passwd=self.mysql_passwd,
            db=self.mysql_db,
            charset=self.mysql_charset,
            cursorclass=pymysql.cursors.DictCursor
        )

    def close_spider(self, spider):
        if self.items:
            self.bulk_update_books()
        self.conn.close()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        if len(self.items) >= 500:
            self.bulk_update_books()
        return item

    def bulk_update_books(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(self.sql, self.items)
        except pymysql.err.Error as e:
            self.spider.logger.error(e)
            self.conn.rollback()
        self.conn.commit()
        self.items = []

    def _sql(self):
        keys = list(BookInfo.fields.keys())
        keys.remove('id')
        self.sql = 'UPDATE `books` SET %s WHERE `id` = %%(id)s' % ','.join(['`%s`=%%(%s)s' % (x, x) for x in keys])


class PrintPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info('(%s) %s' % (item['id'], item['name']))
        return item


class CommentsPipeline(object):

    def __init__(self, settings):
        self.mysql_host = settings.get('MYSQL_HOST')
        self.mysql_port = settings.get('MYSQL_PORT', 3306)
        self.mysql_user = settings.get('MYSQL_USER')
        self.mysql_passwd = settings.get('MYSQL_PASSWD')
        self.mysql_db = settings.get('MYSQL_DB')
        self.mysql_charset = settings.get('MYSQL_CHARSET', 'utf8mb4')
        self.items = []
        self._sql()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def open_spider(self, spider):
        self.spider = spider
        self.conn = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            passwd=self.mysql_passwd,
            db=self.mysql_db,
            charset=self.mysql_charset,
            cursorclass=pymysql.cursors.DictCursor
        )

    def close_spider(self, spider):
        if self.items:
            self.bulk_update_comments()
        self.conn.close()

    def process_item(self, item, spider):
        self.items.append([item['book_id'], item['comment']])
        if len(self.items) >= 500:
            self.bulk_update_comments()
        return item

    def bulk_update_comments(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(self.sql, self.items)
        except pymysql.err.Error as e:
            self.spider.logger.error(e)
            self.conn.rollback()
        self.conn.commit()
        self.items = []

    def _sql(self):
        self.sql = 'INSERT INTO comments (book_id, comment) VALUES (%s, %s)'
