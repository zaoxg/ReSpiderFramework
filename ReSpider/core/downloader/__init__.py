from .handlers import DownloadHandler
from ReSpider.http import Request, Response
from .middleware import DownloaderMiddlewareManager
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
        self.middleware = DownloaderMiddlewareManager.from_crawler(spider, observer=self._observer)

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
        process_req = await self.middleware.process_request(request)
        process_resp = None
        if isinstance(process_req, Request):
            # 只有request是<Request>时才会发送
            response = await self.handler.download_request(request)  # 真正的 <Response>
            process_resp = await self.middleware.process_response(request,
                                                                  response)  # 这个response不一定是 <Response>，也有可能是 <Request>
        if isinstance(process_req, Response):
            # 当中间件把<Request>改为<Response>时
            process_resp = await self.middleware.process_response(request, process_req)
        # response = await self.process_response(request, response)  # 这个response不一定是 <Response>，也有可能是 <Request>
        return process_resp
