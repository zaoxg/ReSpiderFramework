# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:44
# @Author  : ZhaoXiangPeng
# @File    : __init__.py

import os, sys
import re

from ReSpider import setting
from ReSpider.core.spiders.spider import Spider
from ReSpider.extend.redis.spider import RedisSpider
# from .core.spiders.auto_spider import AutoSpider

from ReSpider.http import Request, Response
from ReSpider.extend import PuppeteerRequest, PuppeteerResponse

from ReSpider.core import item

# 添加作用域, 神奇的操作
sys.path.insert(0, re.sub(r'([\\/]items$)|([\\/]spiders$)', '', os.getcwd()))

__all__ = [
    'Spider',
    'RedisSpider',
    'Request',
    'Response',
    'PuppeteerRequest',
    'PuppeteerResponse',
    'item'
]