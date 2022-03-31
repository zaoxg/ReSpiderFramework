from .handlers import DownloadHandler
from ReSpider.http import Request, Response
from ReSpider.middlewares import MiddlewareManager
# from .middleware import DownloaderMiddlewareManager
from ReSpider.extend.logger import LogMixin
from ReSpider.core.observer import Observer


class Downloader(LogMixin):
    name = 'downloader'

    def __init__(self, spider, **kwargs):
        super().__init__(spider)
        self._observer: Observer = kwargs.pop('observer', None)
        # if self._observer:
        #     self._observer.register(self)
        self.handler = DownloadHandler.from_crawler(spider, observer=self._observer)
        self.middleware = DownloaderMiddleware.from_crawler(spider, observer=self._observer)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        return cls.from_settings(spider, **kwargs)

    @classmethod
    def from_settings(cls, spider, **kwargs):
        return cls(spider, **kwargs)

    def open_spider(self, spider):
        pass

    def close_spider(self):
        pass

    async def fetch(self, request):
        """
        下载器拿到 <Request> 后经过中间件处理
        发送请求 -> 获取响应
        拿到 <Response> 经过中间件处理
        :param request:
        :return:
        """
        self._observer.request_count = 1
        # 经过请求中间件处理
        try:
            process_req = await self.middleware.process_request(request)
        except Exception as e:
            # 在出现异常时，任务将重新入队
            self.logger.warning(
                '[%s] Call %s: %s' % (self.__class__.__name__, request, e)
            )
            return request
        process_resp = None
        if isinstance(process_req, Request):
            # 只有request是<Request>时才会发送
            response = await self.handler.download_request(request)  # 真正的 <Response>
            # 获取到 <Response> 后依次经过 process_response
            process_resp = await self.middleware.process_response(request,
                                                                  response)  # 这个response不一定是 <Response>，也有可能是 <Request>
        if isinstance(process_req, Response):
            # 当中间件把 <Request> 改为 <Response> 时
            process_resp = await self.middleware.process_response(request, process_req)
        # response = await self.process_response(request, response)  # 这个response不一定是 <Response>，也有可能是 <Request>
        return process_resp


class DownloaderMiddleware(MiddlewareManager):

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
        if not self.methods['process_request']:
            return request
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
        if not self.methods['process_response']:
            return response
        for mwfn in self.methods['process_response']:
            response = await mwfn(request, response)  # 当异常时这个response是 <Request>
            if isinstance(response, Request):
                # 返回的是<Request>就直接返回
                return request
        if isinstance(response, Response):
            return response
        return response
