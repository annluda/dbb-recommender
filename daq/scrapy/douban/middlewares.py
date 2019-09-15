#! -*- encoding:utf-8 -*-
import random


class TransferProxyMiddleware(object):
    def __init__(self):
        self.proxyServer = "secondtransfer.moguproxy.com:9001"
        self.proxyAuth = "Basic " + "ZlNYVDZtYldMejQ3TWp3ODozWE1uZ2xYSHNQb1MzeWs3"

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxyServer
        request.headers["Authorization"] = self.proxyAuth
        return


class ProxyMiddleware:

    def process_request(self, request, spider):
        with open('/root/scrapy/ips.txt', 'r') as f:
            ip = random.choice(f.readlines())
        request.meta['proxy'] = 'http://' + ip.strip()
        return
