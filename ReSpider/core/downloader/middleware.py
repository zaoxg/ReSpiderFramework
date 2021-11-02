# -*- coding: utf-8 -*-
# @Time    : 2021/8/16 17:41
# @Author  : ZhaoXiangPeng
# @File    : middlewares.py

from ...http import Request, Response
from ...middlewares import MiddlewareManager


class DownloaderMiddlewareManager(MiddlewareManager):

    name = 'downloader middlewares manager'

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return settings.get('DOWNLOADER_MIDDLEWARES', {})

    def _add_middleware(self, mw):
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].append(mw.close_spider)
        if hasattr(mw, 'process_request'):
            self.methods['process_request'].append(mw.process_request)
        if hasattr(mw, 'process_response'):
            self.methods['process_response'].appendleft(mw.process_response)

    async def process_request(self, request):
        """
        让请求过所有中间件的 process_request 方法
        :param request:
        :return:
        """
        if self.methods['process_request']:
            for mwfn in self.methods['process_request']:
                request = await mwfn(request)
                if isinstance(request, Response):
                    # 返回的是<Response>就直接返回
                    return request
        return request

    async def process_response(self, request, response):
        """
        响应先过中间件，如果错误直接返回，最后编码
        :param request:
        :param response:
        :return:
        """
        # 过中间件
        if self.methods['process_response']:
            for mwfn in self.methods['process_response']:
                response = await mwfn(request, response)  # 当异常时这个response是 <Request>
                if isinstance(response, Request):
                    # 返回的是<Request>就直接返回
                    return request
        if isinstance(response, Response):
            return response
        return response
