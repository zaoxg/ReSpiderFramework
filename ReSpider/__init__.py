# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:44
# @Author  : ZhaoXiangPeng
# @File    : __init__.py

from .core.spiders.spider import Spider
from .extend.redis.spider import RedisSpider
# from .core.spiders.auto_spider import AutoSpider

from .http import Request, Response
from .extend import PuppeteerRequest, PuppeteerResponse

from .extend import item
