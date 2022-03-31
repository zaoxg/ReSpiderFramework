# -*- coding: utf-8 -*-
# @Time    : 2022/3/30 9:09
# @Author  : ZhaoXiangPeng
# @File    : mongodb.py

import asyncio
from urllib import parse
import ReSpider.setting as setting
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError
import logging
logger = logging.getLogger(__name__)

__all__ = [
    "AsyncMongoDB"
]


class AsyncMongoDB:
    def __init__(self, host=None, port=None, db=None,
                 username=None, password=None,
                 url=None, loop=None, **kwargs):
        self._loop = loop
        if url:
            self.get_mongo(url)
        else:
            if host is None:
                self._host = setting.MONGODB_HOST
            if port is None:
                self._port = setting.MONGODB_PORT
            if db is None:
                self._db = setting.MONGODB_DB
            if username is None:
                self._username = setting.MONGODB_USERNAME
            if password is None:
                self._password = setting.MONGODB_PASSWORD
            self.get_mongo()

    @classmethod
    def from_url(cls, url, **kwargs):
        """
        mongodb://username:password@host:port
        解析还是直接传呢"""
        if parse.urlparse(url).scheme != 'mongodb':
            raise ValueError('url error, please use "mongodb://username:password@host:port"')
        return cls(url=url, **kwargs)

    def get_mongo(self, url: str = None):
        # 创建对数据库的引用不会执行I/O，不需要 await 表达式
        loop = self._loop or asyncio.get_event_loop()
        if url:
            self._clint: AsyncIOMotorClient = AsyncIOMotorClient(url, io_loop=loop)
        else:
            self._clint: AsyncIOMotorClient = AsyncIOMotorClient(self._host, self._port, io_loop=loop)
        self._db: AsyncIOMotorDatabase = self._clint.get_database(self._db)

    def get_collection(self, coll_name) -> AsyncIOMotorCollection:
        return self._db[coll_name]

    async def add(self, coll_name: str, data: dict):
        """
        :param coll_name: 集合名
        :param data: 单条数据 {'_id': 'xx'}
        :return: 插入影响的行数
        """
        collection = self.get_collection(coll_name)
        affect_count = None
        try:
            result = await collection.insert_one(data)
        except DuplicateKeyError as dup:
            logger.info(
                """
                error: %s
                """ % dup)
        except Exception as e:
            logger.warning('error: %s' % e)
        else:
            affect_count = len(result.inserted_id)
        return affect_count

    async def add_batch(self, coll_name: str, datas: list):
        """
        :param coll_name: 集合名
        :param datas: 多条数据 [{'_id': 'xx'}, ...]
        :return: 插入影响的行数
        """
        collection = self.get_collection(coll_name)
        affect_count = None
        try:
            result = await collection.insert_many(datas)
        except DuplicateKeyError as dup:
            logger.info(
                """
                error: %s
                """ % dup)
        except Exception as e:
            logger.warning('error: %s' % e)
        else:
            affect_count = len(result.inserted_ids)
        return affect_count

    async def delete(self, coll_name: str, condition: dict = None):
        """
        :param coll_name: 集合名
        :param condition: 删除条件 {'i': {'$gt': 1000}}
        :return: 删除的条数
        """
        if condition is None:
            condition = {}
        collection = self.get_collection(coll_name)
        count = await collection.count_documents(condition)
        try:
            result = await collection.delete_one(condition)
        except Exception as e:
            logger.warning(
                """
                error: %s
                condition: %s
                count: %s
                """ % (e, condition, count))
            return False
        return result.deleted_count

    async def update(self, coll_name: str, data: dict, condition: dict = None, upsert: bool = False):
        """
        :param coll_name: 集合名
        :param condition: 更新条件 {'i': {'$gt': 1000}}
        :param data: 修改的值 {'$set': {'key': 'value'}}
        :param upsert: 不存在则插入
        :return: 满足条件的条数
        """
        if condition is None:
            condition = {}  # 如果条件为空将会查找所有
        collection = self.get_collection(coll_name)
        try:
            result = await collection.update_one(condition, {'$set': data}, upsert=upsert)
        except Exception as e:
            logger.warning(
                """
                error: %s
                condition: %s
                """ % (e, condition))
            return False
        return result.modified_count

    async def find(self, coll_name: str, condition: dict = None, limit: int = 0, **kwargs):
        """
        :param coll_name: 集合名
        :param condition: 查询条件 {'i': {'$lt': 4}}
        :param limit: 结果数量
        :return: 插入影响的行数
        """
        condition = {} if condition is None else condition
        collection = self.get_collection(coll_name)
        results = []
        if limit == 1:
            return await collection.find_one(condition)
        elif limit > 1:
            cursor = await collection.find(condition)
            for document in await cursor.to_list(length=limit):
                results.append(document)
        else:
            find_results = collection.find(condition)
            async for document in find_results:
                results.append(document)
        return results

    async def count(self, coll_name: str, condition: dict):
        """
        :param coll_name: 集合名
        :param condition: 查询条件 {'i': {'$gt': 1000}}
        :return: 满足条件的条数
        """
        condition = {} if condition is None else condition
        collection = self.get_collection(coll_name)
        count = await collection.count_documents(condition)
        return count

    async def command(self, command):
        return await self._db.command(command)


if __name__ == '__main__':
    mongo = AsyncMongoDB()
