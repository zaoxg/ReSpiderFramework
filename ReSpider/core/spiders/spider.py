# -*- coding: utf-8 -*-
# @Time    : 2021/8/31 15:12
# @Author  : ZhaoXiangPeng
# @File    : spider.py

from . import Crawler
from ...http import Request


class Spider(Crawler):
    name = 'base_spider'
    __custom_setting__ = {}

    # settings = SettingLoader.from_crawler()

    start_urls = []

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(**kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def start_requests(self):
        if self.start_urls:
            for url in self.start_urls:
                yield Request(url=url)

    async def parse(self, response):
        return response

