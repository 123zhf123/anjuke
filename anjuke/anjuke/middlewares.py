# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import re

import requests
from scrapy import signals
from scrapy.exceptions import IgnoreRequest


class AnjukeSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AnjukeDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def __init__(self):
        self.session = requests.session()
        self.proxy = None

    def process_request(self, request, spider):
        # if self.proxy is None:
        #     self.proxy = self.get_proxy(port=11, spider=spider)
        request.meta['dont_redirect'] = True
        # request.meta['proxy'] = self.proxy

    def process_response(self, request, response, spider):
        if response.status == 302:
            if 'anjuke.com/404' in response.headers['Location'].decode():
                spider.logger.debug('页面不存在: %s' % request.url)
                raise IgnoreRequest()
            input('等待手动通过验证码: %s' % response.headers['Location'].decode())
            request = request.copy()
            return request
        # if 'captcha-verify' in response.url:
        #     spider.logger.debug('出现验证码')
        #     self.proxy = self.get_proxy(port=11, spider=spider)
        #     request = request.copy()
        #     return request
        return response

    def process_exception(self, request, exception, spider):
        # self.proxy = self.get_proxy(port=11, spider=spider)
        return request

    def get_proxy(self, port=1, spider=None):
        url = ('http://webapi.http.zhimacangku.com/getip?num=1&type=2&yys=0&port={}'
               '&time=3&ts=1&ys=0&cs=0&lb=1&sb=0&mr=2&regions=').format(port)
        response = self.session.get(url).json()
        if response['code'] == 0:
            proxy = 'https://%s:%d' % (response['data'][0]['ip'], response['data'][0]['port'])
            spider.logger.debug('获取新的代理IP: %s' % proxy)
            return proxy
        elif response['code'] == 113:
            ip = re.search(r'([\d.]+)', response['msg'])
            if ip:
                ip = ip.group(1)
                self.put_ip_into_white(ip)
                return self.get_proxy(port, spider)

    def put_ip_into_white(self, ip):
        url = ('http://web.http.cnapi.cc/index/index/save_white'
               '?neek=33481&appkey=d212e2fefa6c9648b33f38051fcd9bd5&white={}').format(ip)
        self.session.get(url=url)
