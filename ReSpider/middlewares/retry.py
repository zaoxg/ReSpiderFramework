# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 10:28
# @Author  : ZhaoXiangPeng
# @File    : retry.py

import ReSpider
from ReSpider.middlewares import BaseMiddleware


class RetryMiddleware(BaseMiddleware):
    def __init__(self, spider, **kwargs):
        super().__init__(spider, **kwargs)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        cls.retry_http_codes = spider.settings.get('RETRY_HTTP_CODES', [])
        cls.retry_enabled = spider.settings.get('RETRY_ENABLED', False)
        cls.max_retry_times = spider.settings.get('MAX_RETRY_TIMES', 10)
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
        """
        if len(response.content) < 100 and 'window.location.href' in str(response.content):
            # 这个可能需要先判断响应的大小
            self.logger.debug('<REDIRECT> %s', response.content)
            return await self._retry(request)
        """
        if response.status in self.retry_http_codes:  # 根据状态码判断来决定是否重试
            self.logger.debug(response)
            # self.logger.warning('<CONTENT> %s' % response.content)
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
            self.logger.debug('RETRY...  %s' % request.seen())
            return request
        else:  # 超出最大重试次数后删除指纹
            self.logger.info('MAX RETRY.  \n%s' % request.seen())
            request.meta.setdefault('del_fp', True)
            request.do_filter = True
            request.retry_times = 1
            request.set_fp()  # 重新设置指纹
            return request
