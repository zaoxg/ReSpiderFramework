# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 13:49
# @Author  : ZhaoXiangPeng
# @File    : mysqldb.py

import ReSpider.setting as setting
import aiomysql
import asyncio
import logging
logger = logging.getLogger(__name__)

__all__ = [
    "AsyncMysqlDB"
]


class AsyncMysqlDB:
    def __init__(self,
                 host=None, port=None,
                 user=None, password=None,
                 db=None, loop=None, **kwargs):
        self._host = host or setting.MYSQL_HOST
        self._port = port or setting.MYSQL_PORT
        self._username = user or setting.MYSQL_USERNAME
        self._password = password or setting.MYSQL_PASSWORD
        self._db = db or setting.MYSQL_DB
        self._pool = None
        self._loop = loop
        self.get_mysql()

    @classmethod
    def from_url(cls, url, **kwargs):
        """解析还是直接传呢"""

    def get_mysql(self):
        loop = self._loop or asyncio.get_event_loop()
        task = loop.create_task(self.get_connect())
        loop.run_until_complete(task)

    async def get_connect(self):
        self._pool = await aiomysql.create_pool(
            minsize=1,  # 连接池最小值
            maxsize=32,  # 连接池最大值
            host=self._host,
            port=self._port,
            user=self._username,
            password=self._password,
            db=self._db,
            autocommit=False,  # 自动提交模式
        )

    @property
    def pool(self):
        if self._pool is None:
            self.get_mysql()
        return self._pool

    async def get_cursor(self):
        conn = await self.pool.acquire()
        cursor = await conn.cursor()
        return conn, cursor

    def close_mysql(self):
        loop = self._loop or asyncio.get_event_loop()
        task = loop.create_task(self.close_connect())
        loop.run_until_complete(task)

    async def close_connect(self):
        self._pool.close()
        await self._pool.wait_closed()

    async def release(self, conn=None):
        await self.pool.release(conn)

    async def execute(self, sql):
        affect_count = None
        conn, cursor = await self.get_cursor()
        await conn.begin()
        try:
            affect_count = await cursor.execute(sql)
            await conn.commit()
        except Exception as e:
            await conn.rollback()  # 回滚
            logger.warning(
                """
                error: %s
                sql:   %s
                """ % (e, sql), exc_info=True)
        finally:
            if cursor:
                await cursor.close()
            # 释放掉conn,将连接放回到连接池中
            await self.release(conn)
        return affect_count

    async def executemany(self, sql, datas):
        affect_count = None
        conn, cursor = await self.get_cursor()
        try:
            affect_count = await cursor.executemany(sql, datas)
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            logger.warning(
                """
                error: %s
                sql:   %s
                """ % (e, sql), exc_info=True)
        finally:
            await self.release(conn)
        return affect_count

    async def add(self, sql):
        return await self.execute(sql)

    async def add_batch(self, sql, datas):
        """
        @summary: 批量添加数据
        ---------
        @ param sql: insert ignore into (xxx,xxx) values (%s, %s, %s)
        # param datas: 列表 [{}, {}, {}]
        ---------
        @result: 添加行数
        """
        return await self.executemany(sql, datas)

    def delete(self):
        pass

    async def update(self, sql):
        return await self.execute(sql)

    async def find(self, sql, limit: int = 0, to_json: bool = False):
        conn, cursor = await self.get_cursor()
        await cursor.execute(sql)
        if limit == 1:
            result = await cursor.fetchone()  # 全部查出来，截取 不推荐使用
        elif limit > 1:
            result = await cursor.fetchmany(limit)  # 全部查出来，截取 不推荐使用
        else:
            result = await cursor.fetchall()
        if to_json:
            columns = [i[0] for i in cursor.description]
        await self.release(conn)
        return result
