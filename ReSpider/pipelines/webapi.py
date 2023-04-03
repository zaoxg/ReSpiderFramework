# -*- coding: utf-8 -*-
# @Time    : 2023/2/23 13:35
# @Author  : zhaoxiangpeng
# @File    : webapi.py

import ReSpider.setting as setting
from ReSpider.pipelines import BasePipeline
from ReSpider.item import Item, WebApiItem


class WebApiPipeline(BasePipeline):
    async def process_item(self, item: WebApiItem, spider):
        pass
