# -*- coding: utf-8 -*-
import random
from .user_agents import agents

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = random.choice(agents)

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# HTTPERROR_ALLOWED_CODES = [404]
# HTTPERROR_ALLOW_ALL = False

LOG_LEVEL = 'INFO'
DOWNLOAD_TIMEOUT = 10
RETRY_ENABLED = False
REDIRECT_ENABLED = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False


# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#    'doubhan.middlewares.DoubanSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
   'douban.middlewares.ProxyMiddleware': 100,
}

# Configure item pipelines
ITEM_PIPELINES = {
   # 'douban.pipelines.MysqlPipeline': 300,
   # 'douban.pipelines.PrintPipeline': 200,

   'douban.pipelines.CommentsPipeline': 300,
}


# mysql配置
MYSQL_HOST = '10.0.13.230'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'anluda@1234'
MYSQL_DB = 'douban'
MYSQL_CHARSET = 'utf8mb4'

