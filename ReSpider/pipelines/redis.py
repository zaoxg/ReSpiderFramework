# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 9:11
# @Author  : ZhaoXiangPeng
# @File    : redis.py

from ..pipelines import BasePipeline
from ..extend.item import RdsItem
import redis
import json


class RedisPipeline(BasePipeline):
    """
    redis管道
    需要实现字符串、list、map
    """
    name = 'redis pipelines'

    def __init__(self, settings, spider):
        super().__init__(spider)
        self._pool = redis.ConnectionPool(host=self.redis_host,
                                          port=self.redis_port,
                                          password=self.redis_password,
                                          db=self.redis_db)
        self._r = redis.Redis(connection_pool=self._pool)
        self._keys = spider.name or spider.__class__.name or spider.__class__.__name__

    @classmethod
    def open_spider(cls, settings, spider=None):
        cls.redis_host = settings.get('REDIS_HOST', '127.0.0.1')
        cls.redis_port = settings.get('REDIS_PORT', 6379)
        cls.redis_password = settings.get('REDIS_PASSWORD', None)
        cls.redis_db = settings.get('REDIS_DB', 0)
        return cls(settings, spider)

    @classmethod
    def from_crawler(cls, spider):
        return cls.open_spider(spider.settings, spider)

    async def process_item(self, item: RdsItem, spider):
        keys = f'{self._keys}:{item.rds_type}'
        if item.keys:
            keys = f'{self._keys}:{item.keys}'
        if item.rds_type == 'LIST':
            self._r.rpush(keys, json.dumps(item))
            pass
        elif item.rds_type == 'SET':
            # Todo: 实现的话可能需要修改类型
            pass
        elif item.rds_type == 'HASH':
            # Todo
            # 实现的话可能需要修改类型
            pass
        return item

    def _rpush(self, item, keys=None):
        """
        # 从右边插入一个item
        # Todo: 插入多个
        :param item: 一条数据
        :param keys: redis 键
        :return:
        """
        arg = self._r.rpush(keys, json.dumps(item))
        return arg
