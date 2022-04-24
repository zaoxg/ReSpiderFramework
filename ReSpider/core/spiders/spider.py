# -*- coding: utf-8 -*-
# @Time    : 2021/8/31 15:12
# @Author  : ZhaoXiangPeng
# @File    : spider.py

from . import Crawler
from ReSpider.http import Request


class Spider(Crawler):
    name = 'spider'
    __custom_setting__ = {}
    start_urls = []

    def start_requests(self):
        if self.start_urls:
            for url in self.start_urls:
                yield Request(url=url)

    async def parse(self, response):
        return response

