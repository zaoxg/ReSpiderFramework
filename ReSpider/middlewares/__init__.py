# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:44
# @Author  : ZhaoXiangPeng
# @File    : __init__.py.py

import importlib
from collections import defaultdict, deque
import ReSpider.setting as setting
from ..extend.logger import LogMixin
from ..extend.misc import load_object
from ..core.observer import Observer


class BaseMiddleware(LogMixin):
    name = 'base middleware'

    def __init__(self, spider, **kwargs):
        super().__init__(spider)
        self._observer: Observer = kwargs.pop('observer', None)
        if self._observer:
            self._observer.register(self, default='middleware')

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        return cls(spider, **kwargs)

    def open_spider(self, spider=None, **kwargs):
        return True

    def close_spider(self, spider=None, **kwargs):
        pass

    async def process_request(self, request):
        return request

    async def process_response(self, request, response):
        return response


class MiddlewareManager(LogMixin):
    name = 'middlewares manager'

    def __init__(self, spider=None, *middlewares, **kwargs):
        super().__init__(spider)
        self.logger.debug('MIDDLEWARES START INIT ...')
        self._observer = kwargs.pop('observer', None)
        if self._observer:
            self._observer.register(self)
        self.spider = spider
        self.middleware_list = middlewares
        self.methods = defaultdict(deque)
        for middleware in middlewares:
            mwname = middleware.__class__.__name__
            self.logger.debug('"%s" MIDDLEWARE START INIT ...' % mwname)
            self._add_middleware(middleware)
            self.logger.debug('"%s" MIDDLEWARE INIT SUCCESS.' % mwname)
        self.logger.debug('MIDDLEWARES INIT SUCCESS.')

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        return cls.from_settings(setting.__dict__, spider, **kwargs)

    @classmethod
    def from_settings(cls, settings, spider=None, **kwargs):
        mwlist = cls._get_mwlist_from_settings(settings)
        mws = sorted(mwlist.items(), key=lambda item: item[1])  # 通过排序来确定经过中间件的顺序
        mwlist = dict(mws)
        middlewares = []
        for clspath in mwlist:
            mwcls = load_object(clspath)
            # cls.logger.debug(f'{mwcls} START INIT... ')
            mw = mwcls.from_crawler(spider, **kwargs)
            # cls.logger.debug(f'{mwcls} INIT SUCCESS.')
            middlewares.append(mw)
        return cls(spider, *middlewares, **kwargs)

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        # 继承需要实现这个方法来加载中间件
        raise NotImplementedError

    def loader(self):
        """
        加载器，加载所有的中间件
        返回一个中间件<list>
        :return:
        """
        mws = self.settings.get('DOWNLOADER_MIDDLEWARE', {})
        mws = sorted(mws.items(), key=lambda item: item[1])  # 通过排序来确定经过中间件的顺序
        for md_key, md_value in mws:
            from_package = md_key.rsplit('.', maxsplit=1)
            from_module = from_package[0]
            # from_cls = from_package[1]
            middleware_module = importlib.import_module(from_module)
            for _, obj in middleware_module.__dict__.items():
                # 遍历module，对象是class(type)且是BaseMiddleware的子类并且不是类本身，那么就是{*}Middleware
                if type(obj).__name__ == 'type' and issubclass(obj, BaseMiddleware) and obj.__name__ not in BaseMiddleware.__name__:
                    # print(obj.__module__, obj.__name__)
                    pkn = ".".join([obj.__module__, obj.__name__])
                    self.logger.debug(f'{pkn} START INIT ... ')
                    self._add_middleware(obj.from_crawler(self.spider))
                    self.logger.debug(f'{pkn} INIT SUCCESS.')
        # print(self.middleware_list)

    def _add_middleware(self, mw):
        # self.middleware_list.append(mw)
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].appendleft(mw.close_spider)

    async def process_chain(self, methodname, obj, spider=None):
        for mwfn in self.methods[methodname]:
            pass

    def _process_parallel(self, methodname, spider=None):
        for mwfn in self.methods[methodname]:
            mwfn(spider)

    def open_spider(self, spider=None):
        self.logger.debug('Process parallel "open_spider"')
        return self._process_parallel('open_spider', spider or self.spider)

    def close_spider(self, spider=None):
        self.logger.debug('Process parallel "close_spider"')
        return self._process_parallel('close_spider', spider or self.spider)
