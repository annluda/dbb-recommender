# -*- coding: utf-8 -*-
import requests
import zlib
import time
from lxml import etree
from threading import Thread
from queue import Queue
from daq.subject.mysql_operation import bulk_insert_into_books


class SitemapSpider(Thread):
    def __init__(self, url_queue):
        super(SitemapSpider, self).__init__()
        self.url_queue = url_queue

    def run(self):
        print(self.name, 'start')
        while not self.url_queue.empty():
            self.books()
        return

    def books(self):
        s_time = time.time()
        sitemap = self.url_queue.get()
        response = requests.get(sitemap)  # 返回的.gz需要解压
        data = zlib.decompress(response.content, 16 + zlib.MAX_WBITS)

        # 利用xpath取出所有URL
        selector = etree.HTML(data)
        urls = selector.xpath('//loc/text()')

        data = [a.split('/')[4] for a in urls if a.startswith('https://book.douban.com/subject/')]
        bulk_insert_into_books(data)

        e_time = time.time()
        print(sitemap, '耗时 %dmin%02ds' % divmod(e_time - s_time, 60))
        print(self.url_queue.qsize(), 'left')


def sitemap_index():
    url = 'https://www.douban.com/sitemap_index.xml'
    response = requests.get(url)
    selector = etree.HTML(response.content)
    sitemaps = selector.xpath('//loc/text()')
    return sitemaps


if __name__ == '__main__':

    # 创建序列 存入所有sitemap url
    maps = sitemap_index()
    sitemap_queue = Queue(len(maps))
    for m in maps:
        sitemap_queue.put(m)

    # 启多线程
    t1 = time.time()
    spider_list = []
    for i in range(10):
        spider = SitemapSpider(sitemap_queue)
        spider.start()
        spider_list.append(spider)
    for spider in spider_list:
        spider.join()

    t2 = time.time()
    print(u'总耗时 %dmin%02ds' % divmod(t2 - t1, 60))
