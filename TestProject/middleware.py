# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 22:33
# @Author  : ZhaoXiangPeng
# @File    : middleware.py

from ReSpider.middlewares import BaseMiddleware
import requests
import ReSpider


class RequestMiddleware(BaseMiddleware):
    async def process_request(self, request):
        req = ReSpider.Request('http://127.0.0.1:8000/')
        return await req()
