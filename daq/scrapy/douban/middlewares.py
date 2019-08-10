#! -*- encoding:utf-8 -*-
from twisted.internet.error import ConnectionRefusedError
from twisted.internet.error import TimeoutError
from twisted.internet.error import TCPTimedOutError
from .spiders import db_query


class ProxyMiddleware(object):
    def __init__(self):
        self.ip = ''

    def process_request(self, request, spider):
        self.ip = db_query.query('select ip from proxy_ip')[0][0]
        request.meta['proxy'] = 'http://' + self.ip.strip()
        return

    def process_exception(self, request, exception, spider):
        if isinstance(exception, (ConnectionRefusedError, TimeoutError, TCPTimedOutError)):
            pass
        else:
            spider.logger.warn(type(exception))
        self.ip = db_query.query('select ip from proxy_ip')[1][0]
        request.meta['proxy'] = 'http://' + self.ip.strip()
        return request
