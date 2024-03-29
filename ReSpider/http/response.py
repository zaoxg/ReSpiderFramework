from urllib.parse import urljoin
import cchardet
import json
from parsel import Selector


class Response:
    __text = None
    __selector = None

    def __init__(
            self,
            url, status=200,
            headers=None, cookies=None,
            content=b'', text=None,
            request=None,
            exception=None, *args, **kwargs):
        """
        :param url: <URL>object 响应的URL
        :param status: <int> 响应状态码, 6xx/9xx为自定义的状态码, 多为各种异常
        :param headers: <> 由服务端返回响应的头
        :param cookies: 由服务端返回的cookie, 一般为 Response Headers 的Set-Cookie字段
        :param content: <bytes> 响应的源码
        :param text: <str> 响应的字符串格式源码
        :param request: <Request> 获得此 Response 所发起请求的 Request
        :param exception: 异常, 目前只在错误状态码时使用
        """
        self.url = url
        self.status = status
        self.headers = headers or {}
        self.cookies = cookies
        self.content = content
        self.encoding = None
        # self.text = text
        self.request = request
        self.meta = request.meta if request else None
        self.exception = exception
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def __str__(self):
        return f"<Response [{self.status}]>"

    __repr__ = __str__

    @property
    def apparent_encoding(self):
        return cchardet.detect(self.content).get('encoding', 'utf-8')

    def urljoin(self, val):
        return urljoin(str(self.url), val)

    @property
    def text(self):
        if self.__text is None:
            encoding = self.encoding
            if not self.content:
                return str('')

            if encoding is None:
                self.encoding = self.apparent_encoding

            try:
                self.__text = str(self.content, self.encoding, errors='replace')
            except (LookupError, TypeError):
                # A LookupError is raised if the encoding was not found which could
                # indicate a misspelling or similar mistake.
                #
                # A TypeError can be raised if encoding is None
                #
                # So we try blindly encoding.
                self.__text = str(self.content, errors='replace')
        return self.__text

    def json(self, **kwargs):
        if not self.encoding and self.content and len(self.content) > 3:
            # No encoding set. JSON RFC 4627 section 3 states we should expect
            # UTF-8, -16 or -32. Detect which one to use; If the detection or
            # decoding fails, fall back to `self.text` (using chardet to make
            # a best guess).
            encoding = self.apparent_encoding
            if encoding is not None:
                try:
                    return json.loads(
                        self.content.decode(encoding), **kwargs
                    )
                except UnicodeDecodeError:
                    # Wrong UTF codec detected; usually because it's not UTF-8
                    # but some other 8-bit codec.  This is an RFC violation,
                    # and the server didn't bother to tell us what codec *was*
                    # used.
                    pass
        return json.loads(self.text, **kwargs)

    @property
    def cookiejar(self):
        cookiejar = {}
        cookie_jar = self.cookies.items() if self.cookies else {}
        for _, value in cookie_jar:
            k = value.key
            v = value.value
            cookiejar.update({k: v})
        return cookiejar

    @property
    def selector(self):
        domTree = """
        <html>
        <head>
        </head>
        <body>
        </body>
        </html>
        """  # 构造一个空的DOM树，解决NoneType 没有xpath属性
        if self.__selector is None:
            text = self.text or domTree
            self.__selector = Selector(text)
        return self.__selector

    def xpath(self, query, **kwargs):
        return self.selector.xpath(query, **kwargs)

    def css(self, query):
        return self.selector.css(query)

    def re(self, regex, replace_entities=True):
        return self.selector.re(regex, replace_entities)

    def re_first(self, regex, default=None, replace_entities=True):
        return self.selector.re_first(regex, default, replace_entities)

    def set_request(self, request):
        """
        先保留吧
        把Request注册到Response
        :return:
        """
        self.request = request
