# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 13:49
# @Author  : ZhaoXiangPeng
# @File    : mysqldb.py

import ReSpider.setting as setting
import aiomysql
import asyncio


class MysqlDB:
    def __init__(self,
                 host=None, port=None,
                 user=None, password=None,
                 db=None):
        if host is None:
            self._host = setting.MYSQL_HOST
        if port is None:
            self._port = setting.MYSQL_PORT
        if user is None:
            self._username = setting.MYSQL_USERNAME
        if password is None:
            self._password = setting.MYSQL_PASSWORD
        if db is None:
            self._db = setting.MYSQL_DB
        self._pool = None
        self.get_mysql()

    def get_mysql(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.get_connect())
        loop.run_until_complete(task)

    async def get_connect(self):
        self._pool = await aiomysql.create_pool(
            minsize=5,  # 连接池最小值
            maxsize=10,  # 连接池最大值
            host=self._host,
            port=self._port,
            user=self._username,
            password=self._password,
            db=self._db,
            autocommit=False,  # 自动提交模式
        )

    async def get_cursor(self):
        conn = await self._pool.acquire()
        cur = await conn.cursor(aiomysql.DictCursor)
        return conn, cur

    async def excute(self, sql):
        conn, cur = await self.get_cursor()
        await conn.begin()
        try:
            await cur.execute(sql)
            await conn.commit()
        except Exception:
            await conn.rollback()  # 回滚
        finally:
            if cur:
                await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self._pool.release(conn)

    def add(self, sql):
        conn, cur = await self.get_cursor()
        await conn.begin()
        try:
            await cur.execute(sql)
            await conn.commit()
        except Exception:
            await conn.rollback()  # 回滚
        finally:
            if cur:
                await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self._pool.release(conn)

    def delete(self):
        pass

    def update(self):
        pass

    def find(self):
        pass


if __name__ == '__main__':
    mysql = MysqlDB()
    mysql.add()
