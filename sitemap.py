# -*- coding: utf-8 -*-
import requests
import gzip
import time
from lxml import etree
from threading import Thread
from queue import Queue
from models.tags import Tags
from models.books import Books


class SitemapSpider(Thread):
    def __init__(self, name, url_queue):
        super(SitemapSpider, self).__init__()
        self.name = name
        self.url_queue = url_queue

    def run(self):
        print(self.name, 'started')
        while not self.url_queue.empty():
            self.books()

    def books(self):
        s_time = time.time()
        sitemap = self.url_queue.get()
        response = requests.get(sitemap)
        data = gzip.decompress(response.content)
        selector = etree.HTML(data)
        urls = selector.xpath('//loc/text()')
        for url in urls:
            if url.startswith('https://book.douban.com/tag/'):
                tag = Tags(tag=url.split('/')[4])
                tag.upload()
            elif url.startswith('https://book.douban.com/subject/'):
                book = Books(id=url.split('/')[4])
                book.upload()
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

    maps = sitemap_index()
    sitemap_queue = Queue(len(maps))
    for m in maps:
        sitemap_queue.put(m)

    t1 = time.time()
    spider_list = []
    for i in range(10):
        spider = SitemapSpider('spider' + str(i), sitemap_queue)
        spider.start()
        spider_list.append(spider)
    for spider in spider_list:
        spider.join()

    print('all finished')
    t2 = time.time()
    print('总耗时 %dmin%02ds' % divmod(t2 - t1, 60))
