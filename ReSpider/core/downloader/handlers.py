# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 10:18
# @Author  : ZhaoXiangPeng
# @File    : handlers.py

import sys
import aiohttp
import ReSpider.setting as setting
from ReSpider.http import Response
from ReSpider.extend.logger import LogMixin
from ._ssl import SSLFactory
if sys.version_info >= (3, 8):
    from asyncio.exceptions import TimeoutError
else:
    from asyncio import TimeoutError

sslgen = SSLFactory()


class DownloadHandler(LogMixin):
    def __init__(self, spider, **kwargs):
        super().__init__(spider)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        cls._observer: object = kwargs.pop('observer', None)
        return cls(spider, **kwargs)

    async def download_request(self, request):
        self.logger.debug(request)
        kwargs = {}
        if request.headers:
            headers = request.headers
        else:
            headers = {
                'User-Agent': setting.DEFAULT_USER_AGENT
            }
        kwargs.setdefault('headers', headers)
        kwargs.setdefault('params', request.params)
        kwargs.setdefault('data', request.data)
        kwargs.setdefault('allow_redirects', request.allow_redirects)
        kwargs.setdefault('timeout', aiohttp.ClientTimeout(total=request.timeout))
        kwargs.setdefault('proxy', request.proxy)
        if setting.SSL_FINGERPRINT:
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
            except TimeoutError as timeout_error:
                self._observer.request_count_fail = 1
                self.logger.warning('TimeoutError: %s' % timeout_error)
                return Response(url=request.url,
                                status=601,
                                request=request,
                                exception=timeout_error)
            except aiohttp.ClientConnectorError as client_conn_error:
                self._observer.request_count_fail = 1
                self.logger.warning(client_conn_error)
                return Response(url=request.url,
                                status=602,
                                request=request,
                                exception=client_conn_error)
            except aiohttp.InvalidURL as invalid_url:
                self._observer.request_count_fail = 1
                self.logger.warning(invalid_url)
                return Response(url=request.url,
                                status=603,
                                request=request,
                                exception=invalid_url)
            except aiohttp.ClientHttpProxyError as proxy_error:
                self._observer.request_count_fail = 1
                self.logger.warning(proxy_error)
                return Response(url=request.url,
                                status=604,
                                request=request,
                                exception=proxy_error)
            except aiohttp.ServerDisconnectedError as server_disconnected_error:
                self._observer.request_count_fail = 1
                self.logger.warning(server_disconnected_error)
                return Response(url=request.url,
                                status=605,
                                request=request,
                                exception=server_disconnected_error)
            except aiohttp.ClientOSError as client_os_error:
                self._observer.request_count_fail = 1
                self.logger.warning(client_os_error)
                return Response(url=request.url,
                                status=606,
                                request=request,
                                exception=client_os_error)
            except Exception as exception:
                self._observer.request_count_fail = 1
                self.logger.warning(request.cat())
                self.logger.error(exception, exc_info=True)
                return Response(url=request.url,
                                status=999,
                                request=request,
                                exception=exception)
