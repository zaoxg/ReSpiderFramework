# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 15:37
# @Author  : ZhaoXiangPeng
# @File    : mysql.py

from ReSpider.utils.tools import make_sql_insert, make_sql_update
import ReSpider.setting as setting
from ReSpider.core.item import MysqlItem
from ..db.mysqldb import MysqlDB
from . import BasePipeline
import re


class MySQLPipeline(BasePipeline):
    name = 'mysql pipeline'

    def open_spider(self, spider=None, **kwargs):
        self._mysql = MysqlDB()

    async def process_item(self, item: MysqlItem, spider):
        table = item.table
        sql = make_sql_insert(table, item)
        self._mysql.add(sql)
