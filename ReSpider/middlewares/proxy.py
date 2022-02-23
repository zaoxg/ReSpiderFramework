from ..middlewares import BaseMiddleware
import ReSpider.setting as setting


class ProxyMiddleware(BaseMiddleware):
    @classmethod
    def from_crawler(cls, spider, **kwargs):
        return cls(spider, **kwargs)

    def open_spider(self, spider=None, **kwargs):
        self.get_proxy()

    async def process_request(self, request):
        try:
            proxy = self.proxys.pop()
        except IndexError:
            self.logger.warning('没有可以使用的ip')
            proxy = ''
        else:
            request.proxy = proxy
        # self.logger.info(request.seen())
        return request

    async def process_response(self, request, response):
        if response.status == 200:
            self.proxys.append(request.proxy)
        return response

    def get_proxy(self):
        import requests
        self.proxys = requests.get(setting.PROXY_POOL_URL).json()
        self.proxys = [f'http://{proxy.get("proxy")}' for proxy in self.proxys]
