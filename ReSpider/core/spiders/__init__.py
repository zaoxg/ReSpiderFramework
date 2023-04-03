# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:51
# @Author  : ZhaoXiangPeng
# @File    : __init__.py

import ReSpider.setting as setting
from ReSpider.utils.tools import hump2underline
from ReSpider.extend.logger import LogMixin


class Crawler(LogMixin):
    name = 'crawler'
    __custom_setting__ = {}
    start_urls = []

    def __init__(self, **kwargs):
        self.name = hump2underline(self.__class__.__name__)

        # 更新自定义配置到setting
        for key, val in self.__class__.__custom_setting__.items():
            if setting.__dict__.get(key).__class__ == dict:
                getattr(setting, key).update(val)
                continue
            setattr(setting, key, val)
        if not setting.LOG_NAME:
            setattr(setting, 'LOG_NAME', self.name)
        for key, val in kwargs.items():
            if setting.__dict__.get(key):
                setattr(setting, key, val)
                continue
            setattr(self.__class__, key, val)
        super().__init__(self)

        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def __str__(self):
        return '<%s [%s]>' % (self.__class__.__base__.__name__, self.__class__.__name__)

    __repr__ = __str__

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return None

    def start_requests(self):
        raise NotImplementedError

    def parse(self, response):
        raise NotImplementedError

    def start(self):
        self.logger.debug('SPIDER START INIT ...')
        from ReSpider.core.engine import Engine
        engine = Engine(self)
        engine.start()
