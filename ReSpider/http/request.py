from typing import Optional
import ReSpider.setting as setting
from ReSpider.utils import encrypt_md5
import ReSpider.utils.tools as tools
import requests
import aiohttp
from .response import Response


class Request:
    name = 'request'

    def __init__(self, url: Optional[str], method: Optional[str] = None,
                 headers=None, params: dict = None, data=None, cookies=None, allow_redirects: bool = True,
                 encoding: Optional[str] = 'utf-8',
                 proxy='', timeout: Optional[int] = 30,
                 retry: bool = setting.RETRY_ENABLED, max_retry_times: int = setting.MAX_RETRY_TIMES,
                 meta=None,
                 priority: Optional[int] = 1, do_filter: bool = False,
                 callback=None, errback=None, **kwargs):
        if url is None:
            raise ValueError(f'{self.__class__} url Cannot be empty')
        self._set_url(url)
        if method is None:
            self.method = 'GET'
        else:
            self.method = str(method).upper()
        self.headers = headers or {}
        if params is None:
            self.params = {}
        else:
            self.params = params
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.cookies = cookies or {}
        self.allow_redirects = allow_redirects
        self.encoding = encoding or 'utf-8'
        self.proxy = proxy
        self.timeout = timeout
        self.meta = meta
        self.priority = priority  # 优先级
        self.do_filter = do_filter
        if self.do_filter:
            self._set_fingerprint()  # 指纹
        self.retry = retry
        self.retry_times = 0
        self.max_retry_times = max_retry_times
        self.callback = callback
        self.errback = errback
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def __str__(self): return f"<{self.method} {self.url}>"

    __repr__ = __str__

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        return None

    def __lt__(self, other):
        # 自定义的类定义了__lt__, 可以比较大小
        # 解决 TypeError: '<' not supported between instances of 'Request' and 'Request'
        return self.priority < other.priority

    async def __call__(self, *args, **kwargs):
        """
        实现个 asyncio 的 __call__ 异步直接执行，需要在await中使用
        :param args:
        :param kwargs:
        :return:
        """
        kwargs = {}
        kwargs.setdefault('headers', self.headers)
        kwargs.setdefault('params', self.params)
        kwargs.setdefault('data', self.data)
        kwargs.setdefault('allow_redirects', self.allow_redirects)
        kwargs.setdefault('timeout', aiohttp.ClientTimeout(total=self.timeout))
        kwargs.setdefault('proxy', self.proxy)
        async with aiohttp.ClientSession(cookies=self.cookies,
                                         connector=aiohttp.TCPConnector(ssl=False), trust_env=True) as session:
            response = await session.request(method=self.method, url=self.url, **kwargs)
            content = await response.read()
            # print(content)
            return Response(url=response.url,
                            status=response.status,
                            headers=response.headers,
                            cookies=response.cookies,
                            content=content,
                            request=self)

    def _set_url(self, url):
        if not isinstance(url, str):
            raise TypeError(f'Request url must be str or unicode, got {type(url).__name__}')
        if '://' not in url:
            url = 'http://' + url
            # raise ValueError('非法url')
        self.url = url

    @property
    def to_dict(self):
        request_dict = {}
        self.callback = getattr(self.callback, '__name__') if callable(self.callback) else self.callback
        for key, val in self.__dict__.items():
            if (val is not None) and not isinstance(val, (bytes, int, str, float, bool, tuple, list, dict)):
                val = tools.dumps_obj(val)
            request_dict[key] = val
        return request_dict

    # @property
    # def do_filter(self):
    #     return self.__do_filter
    #
    # @do_filter.setter
    # def do_filter(self, val: bool):
    #     if self.__do_filter != val:
    #         self.__do_filter = val
    #     if self.__do_filter:
    #         self._set_fingerprint()
        # else:
        #     self.fingerprint = None

    def _set_fingerprint(self):
        # @summery: 没有指纹时才会设置指纹
        if self.fingerprint is None:
            self.fingerprint = encrypt_md5(self.url + str(self.params) + str(self.data))

    def copy(self): return self.replace()

    def cat(self):
        from ReSpider.utils.tools import extract_dict
        return extract_dict(self.__dict__, {'url', 'method', 'headers', 'params', 'data', 'cookies', 'allow_redirects', 'encoding', 'proxy', 'timeout', 'meta', 'priority', 'fingerprint', 'retry', 'retry_times', 'max_retry_times', 'callback', 'errback', 'do_filter'})

    def send(self):
        """
        用requests库进行测试
        """
        u = self.url
        m = self.method
        hd = self.headers.copy()
        if 'user-agent' not in hd and 'User-Agent' not in hd:
            hd.update({'user-agent': setting.DEFAULT_USER_AGENT})
        kwg = {'headers': hd, 'cookies': self.cookies, 'params': self.params, 'data': self.data}
        return requests.request(url=u, method=m, **kwg)

    def replace(self, *args, **kwargs):
        for x in ['url', 'method', 'headers', 'data', 'cookies', 'meta',
                  'encoding', 'priority', 'do_filter', 'callback', 'errback']:
            kwargs.setdefault(x, getattr(self, x))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    @classmethod
    def make_request(cls, request_dict: dict):
        for key, val in request_dict.items():
            if isinstance(val, bytes):
                request_dict[key] = tools.loads_obj(val)
        return cls(**request_dict)
