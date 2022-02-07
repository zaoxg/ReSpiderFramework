from ..middlewares import BaseMiddleware


class ProxyMiddleware(BaseMiddleware):
    @classmethod
    def from_crawler(cls, spider, **kwargs):
        cls.get_proxy()
        return cls(spider, **kwargs)

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

    @classmethod
    def get_proxy(cls):
        import requests
        cls.proxys = requests.get("http://iproxy.zhaoxp.run/get_all/").json()
        cls.proxys = [f'http://{proxy.get("proxy")}' for proxy in cls.proxys]
