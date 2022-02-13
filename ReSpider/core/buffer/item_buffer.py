# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 11:17
# @Author  : ZhaoXiangPeng
# @File    : item_buffer.py

import asyncio
from . import ItemDo

MAX_ITEM_COUNT = 500


class ItemBuffer:

    __BUFFER__ = {
        # MysqlPipeline
        # MongodbPipeline
        # ...
    }

    def add_buffer(self, data: ItemDo):
        pipeline_key = data.pipeline
        if self.__BUFFER__.get(pipeline_key) is None:
            self.__BUFFER__[pipeline_key]: list = []  # 暂时先用list结构存储
        self.__BUFFER__[pipeline_key].append(data)

    def save_data(self):
        pass

    def check_count(self):
        for pipeline, items in self.__BUFFER__.items():
            if items.__len__() > MAX_ITEM_COUNT:
                # do something
                # ...
                self.__BUFFER__[pipeline] = []
