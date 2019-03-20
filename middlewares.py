# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import requests
from datetime import datetime, timedelta


class UAMiddleware:

    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        if self.ua:
            request.headers['User-Agent'] = self.ua.random
        return None

class ProxyMiddleware:

    def __init__(self):
        self.url = 'http://127.0.0.1:5000/random'
        self.no_proxy_time = datetime.now()
        self.limit = 30


    def process_request(self, request, spider):
        if datetime.now() > (self.no_proxy_time + timedelta(seconds=self.limit)):
            if datetime.now() > (self.no_proxy_time + timedelta(seconds=self.limit*2)):
                self.no_proxy_time = datetime.now()
            proxy = requests.get(url=self.url, timeout=3).text
            if proxy:
                print('使用代理: ',proxy)
                request.meta["proxy"] = 'http://' + proxy
        return None

    def process_exception(self, request, exception, spider):
        return request





