# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 15:37
# @Author  : ZhaoXiangPeng
# @File    : mysql.py

from ReSpider.utils.tools import make_sql_insert, make_batch_sql
from ReSpider.item import MysqlItem, MysqlListItem
from ..db.mysqldb import AsyncMysqlDB as MysqlDB
from . import BasePipeline

__all__ = [
    "MySQLPipeline"
]


class MySQLPipeline(BasePipeline):
    name = 'mysql pipeline'

    def open_spider(self, spider=None, **kwargs):
        self._mysql = MysqlDB(loop=self._observer.loop)

    def close_spider(self, spider=None, **kwargs):
        self._mysql.close_mysql()

    async def process_item(self, item: MysqlItem, spider):
        table = item.table
        if isinstance(item, MysqlListItem):
            sql, datas = make_batch_sql(item.table, item)
            add_count = await self._mysql.add_batch(sql, datas)
        else:
            sql = make_sql_insert(table, item)
            add_count = await self._mysql.add(sql)
        if add_count:
            self.logger.info('入库 %s 行数 %s 条, 影响行数 %s 条' % (item.table, len(item), add_count))
        return item
