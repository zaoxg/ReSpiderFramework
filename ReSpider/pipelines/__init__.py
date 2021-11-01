# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:45
# @Author  : ZhaoXiangPeng
# @File    : __init__.py

from ..extend.logger import LogMixin
from ..extend.item import Item
from ..middlewares import MiddleWareManager


class BasePipeline(LogMixin):
    name = 'pipelines'

    @classmethod
    def from_crawler(cls, spider):
        pass

    @classmethod
    def open_spider(cls, settings, spider=None):
        return cls(spider)

    @classmethod
    def close_spider(cls, spider=None):
        pass

    async def process_item(self, item: Item, spider):
        return item


class PipelineManager(MiddleWareManager):

    name = 'pipelines manager'

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return settings.get('ITEM_PIPELINES', {})

    @classmethod
    def from_crawler(cls, spider):
        return cls.from_settings(spider.settings, spider)

    def _add_middleware(self, mw):
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].appendleft(mw.close_spider)
        if hasattr(mw, 'process_item'):
            self.methods['process_item'].append(mw.process_item)

    async def process_chain(self, methodname, item, spider=None):
        # self.logger.debug(item)
        for mwfn in self.methods[methodname]:
            # self.logger.debug(mwfn)
            # 判断 method 的 类名是否与 item 指定的 pipelines 相同
            # True: 去这个 pipelines 处理这个item
            if item.pipeline == mwfn.__self__.__class__.__name__:
                try:
                    item = await mwfn(item, spider)
                except ValueError as ve:
                    self.logger.error(ve, exc_info=True)
                    raise ValueError(ve)
