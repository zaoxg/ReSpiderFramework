# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 10:20
# @Author  : ZhaoXiangPeng
# @File    : httperror.py

from ReSpider.middlewares import BaseMiddleWare


class HttpError:
    pass


class HttpErrorMiddleware(BaseMiddleWare):
    def __init__(self, spider):
        super().__init__()
        self.http_status_list = spider.settings.get('', [])

    def process_response(self, request, response):
        if response.status in self.http_status_list:
            return response

