# -*- coding: utf-8 -*-
# @Time    : 2021/8/31 15:12
# @Author  : ZhaoXiangPeng
# @File    : spider.py

from . import Crawler
from ...http import Request
from ...extend import SettingLoader


class Spider(Crawler):
    name = 'base_spider'

    settings = SettingLoader.from_crawler()

    start_urls = []

    def __init__(self, **kwargs):
        # self.name = name or self.name
        super().__init__()
        # if self.name is not None:
        #     self.name = name
        # else:
        #     self.name = self.__class__.__name__
        self.__dict__.update(**kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def start_requests(self):
        if self.start_urls:
            for url in self.start_urls:
                yield Request(url=url)

    async def parse(self, response):
        return response

