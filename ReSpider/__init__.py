# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:44
# @Author  : ZhaoXiangPeng
# @File    : __init__.py

import os, sys
import re
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

from . import setting
from .core.spiders.spider import Spider
from .extend.redis.spider import RedisSpider
# from .core.spiders.auto_spider import AutoSpider

from .http import Request, Response
from .extend import PuppeteerRequest, PuppeteerResponse

from .extend import item
