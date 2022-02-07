# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 10:20
# @Author  : ZhaoXiangPeng
# @File    : httperror.py

from ReSpider.middlewares import BaseMiddleware
import ReSpider.setting as setting


class HttpError:
    pass


class HttpErrorMiddleware(BaseMiddleware):
    http_status_list = setting.get('', [])

    def process_response(self, request, response):
        if response.status in self.http_status_list:
            return response

