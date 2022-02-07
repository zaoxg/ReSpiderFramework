# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 10:20
# @Author  : ZhaoXiangPeng
# @File    : cookies.py

from ..middlewares import BaseMiddleware
import random


class CookiesMiddleware(BaseMiddleware):
    cookies_pool = []

    async def process_request(self, request):
        cookies = request.cookies
        headers = request.headers
        if cookies:
            return request
        elif 'Cookie' not in headers and 'cookie' not in headers:
            request.cookies = random.choice(self.cookies_pool)
            # if request.headers['Cookie'] == self.cookie:
            #     self.logger.info(request.headers['Cookie'])
            return request
        else:
            return request
