# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 14:27
# @Author  : ZhaoXiangPeng
# @File    : response.py

# from ReSpider import Response
from ...http import Response


class PuppeteerResponse(Response):
    name = 'puppeteer response'

    def __init__(self, url, status=200, headers=None, cookies=None, content=b'', text=None, request=None, *args, **kwargs):
        content = content or bytes(text, encoding='utf-8')
        super().__init__(url, status, headers, cookies, content, text, request, *args, **kwargs)

    @property
    def cookiejar(self):
        cookiejar = {}
        cookie_jar = self.cookies
        for c in cookie_jar:
            cookiejar[c['name']] = c['value']
        return cookiejar
