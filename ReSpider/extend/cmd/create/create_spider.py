# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 16:17
# @Author  : ZhaoXiangPeng
# @File    : create_spider.py

import getpass
import os
from .create_init import CreateInit


class CreateSpider:
    def __init__(self):
        self._create_init = CreateInit()

    def create(self, spider_name, spider_type=None):
        if os.path.exists(spider_name):
            print('%s 爬虫已经存在' % spider_name)
        else:
            print('%s 爬虫创建成功' % spider_name)