from typing import Optional
import ReSpider.setting as setting
from ReSpider.utils import encrypt_md5
import requests


class Request:
    name = 'request'

    def __init__(self, url: Optional[str], method: Optional[str] = None,
                 headers=None, params=None, data=None, cookies=None, allow_redirects: bool = True,
                 encoding: Optional[str] = 'utf-8',
                 proxy='', timeout: Optional[int] = 30,
                 retry: bool = setting.RETRY_ENABLED, max_retry_times: int = setting.MAX_RETRY_TIMES,
                 meta=None,
                 priority: Optional[int] = 1, do_filter: bool = False,
                 callback=None, errback=None, *args, **kwargs):
        if url is None:
            raise ValueError(f'{self.__class__} url Cannot be empty')
        self._set_url(url)
        if method is None:
            self.method = 'GET'
        else:
            self.method = str(method).upper()
        self.headers = headers or {}
        self.params = params or ''
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
        self.fingerprint = None  # 指纹
        self.retry = retry
        self.retry_times = 0
        self.max_retry_times = max_retry_times
        self.callback = callback
        self.errback = errback
        if self.do_filter:
            self._set_fingerprint()

    def _set_url(self, url):
        if not isinstance(url, str):
            raise TypeError(f'Request url must be str or unicode, got {type(url).__name__}')
        if '://' not in url:
            url = 'http://' + url
            # raise ValueError('非法url')
        self.url = url

    def __str__(self):
        return f"<{self.method} {self.url}>"

    def __lt__(self, other):
        # 自定义的类定义了__lt__, 可以比较大小
        # 解决 TypeError: '<' not supported between instances of 'Request' and 'Request'
        return self.priority < other.priority

    __repr__ = __str__

    def copy(self):
        return self.replace()

    def _set_fingerprint(self):
        self.fingerprint = encrypt_md5(self.url + str(self.params) + str(self.data))

    def set_fp(self):
        if self.do_filter:
            self._set_fingerprint()

    def cat(self):
        return self.__dict__

    def send(self):
        """
        用requests库进行测试
        """
        u = self.url
        m = self.method
        hd = self.headers.copy()
        if 'user-agent' not in hd and 'User-Agent' not in hd:
            hd.update({'user-agent': 'PostmanRuntime/7.28.4'})
        kwg = {'headers': hd, 'cookies': self.cookies, 'params': self.params, 'data': self.data}
        return requests.request(url=u, method=m, **kwg)

    def replace(self, *args, **kwargs):
        for x in ['url', 'method', 'headers', 'data', 'cookies', 'meta',
                  'encoding', 'priority', 'do_filter', 'callback', 'errback']:
            kwargs.setdefault(x, getattr(self, x))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    # def __setattr__(self, key, value):
    #     self[key] = value
