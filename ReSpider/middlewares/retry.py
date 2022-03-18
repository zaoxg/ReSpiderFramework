# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 10:28
# @Author  : ZhaoXiangPeng
# @File    : retry.py

import ReSpider
import ReSpider.setting as setting
from ReSpider.middlewares import BaseMiddleware


class RetryMiddleware(BaseMiddleware):
    @classmethod
    def from_crawler(cls, spider, **kwargs):
        cls.retry_http_codes = set(setting.RETRY_HTTP_CODES or [])
        cls.retry_enabled = setting.RETRY_ENABLED or False
        cls.max_retry_times = setting.MAX_RETRY_TIMES or 10
        return cls(spider, **kwargs)

    async def process_request(self, request):
        if self.retry_enabled ^ request.retry is True:
            request.retry = True
        elif (self.retry_enabled is True) and (request.retry is True):
            request.retry = True
        if request.max_retry_times < self.max_retry_times:
            request.max_retry_times = self.max_retry_times
        return request

    async def process_response(self, request, response):
        if request.retry is False:
            # 当重试关闭时，不管响应如何，直接返回
            return response
        if response.status != 200:
            self.logger.debug('Abnormal status code: %s' % response.status)
        if response.status in self.retry_http_codes:  # 根据状态码判断来决定是否重试
            # self.logger.info(response.exception)
            # 出现异常状态码时，去重新处理请求进行重试
            return await self._retry(request)  # 重试的请求 返回 <Request>
        return response

    async def _retry(self, request) -> ReSpider.Request:
        """
        todo 需要在超过最大重试次数时把fingerprint删除
        或者只要失败就删除, 根据<Request>[meta.del_fp]来确定删除和添加
        :param request:
        :return:
        """
        retries = request.retry_times + 1  # 每次重试经过这里 <retry_times> +1
        if retries <= request.max_retry_times:  # 小于指定的最大重试次数就接着请求
            request.retry_times = retries
            request.do_filter = False  # 在重试次数内不去重
            self.logger.info('retry: %s' % request)
            return request
        else:  # 超出最大重试次数后删除指纹
            self.logger.info('Max retry.  \n%s' % request.cat())
            if request.meta is None:
                request.meta = {}
            request.meta.setdefault('del_fp', True)
            request.do_filter = True
            request.retry_times = 1
            request.set_fp()  # 重新设置指纹
            return request
