# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 22:11
# @Author  : ZhaoXiangPeng
# @File    : redisdb.py
# MULTI执行之后，客户端可以继续向服务器发送任意多条命令，这些命令不会立即被执行，而是被放到一个队列中，当EXEC命令被调用时，所有队列中的命令才会被执行

import ReSpider.setting as setting
import redis

__all__ = [
    "RedisDB"
]


class RedisDB:
    def __init__(self,
                 host=None, port=None,
                 db=None,
                 user_pass=None):
        self._host = host or setting.REDIS_HOST
        self._port = port or setting.REDIS_PORT
        self._db = db or setting.REDIS_DB
        self._user_pass = user_pass or setting.REDIS_PASSWORD
        self._redis = None
        self.get_redis()

    def get_redis(self):
        self._pool = redis.ConnectionPool(host=self._host,
                                          port=self._port,
                                          password=self._user_pass,
                                          db=self._db)
        self._redis = redis.Redis(connection_pool=self._pool)

    def keys(self, pattern='*') -> list:
        """
        获取当前库中所有的key
        """
        return self._redis.keys(pattern)

    def sadd(self, table, values):
        """
        set <添加>, 一般用来去重
        :param table: 表名
        :param values: 值, 支持多个值<list>
        :return:
        """
        if isinstance(values, list):
            pipe = self._redis.pipeline()
            pipe.multi()
            for value in values:
                pipe.sadd(table, value)
            pipe.execute()
        else:
            return self._redis.sadd(table, values)

    def rpush(self, table, values):
        """
        LIST <右侧push>
        :param table:
        :param values:
        :return:
        """
        if isinstance(values, list):
            pipe = self._redis.pipeline()
            pipe.multi()
            for value in values:
                pipe.rpush(table, value)
            pipe.execute()
        else:
            return self._redis.rpush(table, values)

    def lpush(self, table, values):
        """
        LIST <左侧push>
        :param table:
        :param values:
        :return:
        """
        if isinstance(values, list):
            pipe = self._redis.pipeline()
            pipe.multi()
            for value in values:
                pipe.lpush(table, value)
            pipe.execute()
        else:
            return self._redis.lpush(table, values)

    def lget_count(self, table):
        # 返回LIST元素数量
        return self._redis.llen(table)

    def lpop(self, table, count=1):
        """
        返回 1 ~ 多个
        :param table:
        :param count: > 1时返回列表, 且不能超出总长度
        :return:
        """
        datas = None
        count = count if self.lget_count(table) >= count else self.lget_count(table)
        if count:  # 首先需要以上条件成立 即有至少1个元素
            if count > 1:
                pipe = self._redis.pipeline()
                pipe.multi()
                while count:
                    # 弹出 <count> 个
                    pipe.lpop(table)
                    count -= 1
                datas = pipe.execute()
            else:
                datas = self._redis.lpop(table)
        return datas

    def hset(self, table, datas):
        """
        HASH 单个值 key, value; 多个 mapping {key1: val1, key2: val2}
        :param table:
        :param datas:
        :return:
        """
        pipe = self._redis.pipeline()
        pipe.multi()
        for key, val in datas:
            pipe.hset(table, key, val)
        return pipe.execute()

    def hgetall(self, table) -> dict:
        """
        获取Hash结构所有的键值对
        {b'a': b'1', b'c': b'2'}
        """
        return self._redis.hgetall(table)

    # ########################################  String结构操作  ########################################

    def get(self, table):
        return self._redis.mget(table)

    def set(self, table, value,
            ex=None, px=None, nx=False, xx=False, keepttl=False):
        return self._redis.set(table, value,
                               ex=ex, px=px, nx=nx, xx=xx, keepttl=keepttl)

    def __getattr__(self, item):
        return getattr(self._redis, item)
