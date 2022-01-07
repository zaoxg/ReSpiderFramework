# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:51
# @Author  : ZhaoXiangPeng
# @File    : __init__.py.py

import ReSpider.setting as setting
from ReSpider.utils.tools import hump2underline
from ..engine import Engine
from ...extend.logger import LogMixin


class Crawler(LogMixin):
    name = 'crawler'
    __custom_setting__ = {}
    start_urls = []

    def __init__(self, **kwargs):
        self.name = hump2underline(self.__class__.__name__)

        # 更新自定义配置到setting
        for key, val in self.__class__.__custom_setting__.items():
            setattr(setting, key, val)
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
