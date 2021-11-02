# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 10:18
# @Author  : ZhaoXiangPeng
# @File    : handlers.py

import sys
import asyncio
from asyncio.exceptions import TimeoutError
import aiohttp

from ._ssl import SSLFactory
from ...http import Response
from ...extend.logger import LogMixin

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sslgen = SSLFactory()


class DownloadHandler(LogMixin):
    def __init__(self, spider, **kwargs):
        super().__init__(spider)
        self._observer = kwargs.pop('observer', None)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        cls.settings = spider.settings
        return cls(spider, **kwargs)

    async def download_request(self, request):
        self.logger.info(request)
        kwargs = {}
        if request.headers:
            headers = request.headers
        elif self.settings.get('headers', False):
            headers = self.settings.get('headers')
        else:
            headers = {}
        kwargs.setdefault('headers', headers)
        kwargs.setdefault('params', request.params)
        kwargs.setdefault('data', request.data)
        kwargs.setdefault('allow_redirects', request.allow_redirects)
        kwargs.setdefault('timeout', aiohttp.ClientTimeout(total=request.timeout))
        kwargs.setdefault('proxy', request.proxy)
        if self.settings.get('SSL_FINGERPRINT', False) is True:
            kwargs.setdefault('ssl', sslgen())

        async with aiohttp.ClientSession(cookies=request.cookies,
                                         connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session:
            try:
                response = await session.request(method=request.method, url=request.url, **kwargs)
                content = await response.read()
                return Response(url=response.url,
                                status=response.status,
                                headers=response.headers,
                                cookies=response.cookies,
                                content=content,
                                request=request)
            except TimeoutError as timeoutError:
                self.logger.error(timeoutError, exc_info=True)
                return Response(url=request.url,
                                status=601,
                                request=request)
            except aiohttp.ClientConnectorError as client_conn_error:
                self.logger.error(client_conn_error, exc_info=True)
                return Response(url=request.url,
                                status=602,
                                request=request)
            except aiohttp.InvalidURL as invalid_url:
                self.logger.error(invalid_url, exc_info=True)
                return Response(url=request.url,
                                status=603,
                                request=request)
            except aiohttp.ClientHttpProxyError as proxy_error:
                self.logger.error(proxy_error, exc_info=True)
                return Response(url=request.url,
                                status=604,
                                request=request)
            except Exception as exception:
                self.logger.warning(request.seen())
                self.logger.error(exception, exc_info=True)
                return Response(url=request.url,
                                status=999,
                                request=request)
