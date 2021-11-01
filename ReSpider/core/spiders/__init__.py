# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:51
# @Author  : ZhaoXiangPeng
# @File    : __init__.py.py

from ..engine import Engine
from ...extend.logger import LogMixin


class Crawler(LogMixin):
    name = 'crawler'
    start_urls = []

    settings = {}

    def __init__(self, **kwargs):
        super().__init__(self)
        self.__dict__.update(**kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def start_requests(self):
        raise NotImplementedError

    def parse(self, response):
        raise NotImplementedError

    def start(self):
        self.logger.info('SPIDER START INIT ...')
        engine = Engine(self)
        engine.start()
