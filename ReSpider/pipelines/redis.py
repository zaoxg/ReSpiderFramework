# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 9:11
# @Author  : ZhaoXiangPeng
# @File    : redis.py

import ReSpider.setting as setting
from ..pipelines import BasePipeline
from ReSpider.core.item import RdsItem
import redis
import json


class RedisPipeline(BasePipeline):
    """
    redis管道
    需要实现字符串、list、map
    """
    name = 'redis pipelines'

    def __init__(self, spider, **kwargs):
        super().__init__(spider, **kwargs)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        # settings = spider.settings
        cls.redis_host = setting.REDIS_HOST
        cls.redis_port = setting.REDIS_PORT
        cls.redis_password = setting.REDIS_PASSWORD
        cls.redis_db = setting.REDIS_DB
        return cls(spider, **kwargs)

    def open_spider(self, spider=None, **kwargs):
        self._pool = redis.ConnectionPool(host=self.redis_host,
                                          port=self.redis_port,
                                          password=self.redis_password,
                                          db=self.redis_db)
        self._r = redis.Redis(connection_pool=self._pool)
        self._key = spider.name or spider.__class__.name or spider.__class__.__name__

    async def process_item(self, item: RdsItem, spider):
        key = f'{self._key}:{item.rds_type}'
        if item.key:
            key = item.key
        if item.rds_type == 'LIST':
            self._r.rpush(key, json.dumps(item))
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
