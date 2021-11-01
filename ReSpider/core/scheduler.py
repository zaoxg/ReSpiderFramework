import asyncio
# from asyncio import Queue
from queue import Queue, PriorityQueue
from queue import Empty
# from ..utils import encrypt_md5
from ..extend import LogMixin


class Scheduler(LogMixin):
    def __init__(self, spider, **kwargs):
        super().__init__(spider)
        self._observer = kwargs.get('observer')
        if self._observer:
            self._observer.register(self)
        # print(self._observer.observers())
        self.spider = spider
        self.settings = spider.settings
        self.queue = PriorityQueue()
        self.df = set()

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        return cls(spider, **kwargs)

    def __len__(self):
        """
        返回队列任务数
        :return:
        """
        return self.queue.qsize()

    def enqueue_request(self, request):
        """
        向队列中插入一个请求
        :param request:
        :return:
        """
        if request.do_filter:
            if self.verify_fingerprint(request):
                self.queue.put_nowait(request)
        else:
            self.queue.put_nowait(request)
        return request

    async def next_request(self):
        """
        获取下一个请求
        :return:
        """
        try:
            request = self.queue.get_nowait()
        except Empty:
            request = None
        # print(type(request))
        return request

    def has_pending_requests(self):
        """
        判断队列中是否有请求
        :return:
        """
        return self.queue.qsize() > 0

    def _srem(self, fp):
        # 从集合删除一个元素
        self.df.remove(fp)

    def verify_fingerprint(self, request):
        """
        先来个指纹
        :return:
        """
        fp = request.fingerprint
        if fp not in self.df:
            self.df.add(fp)
            return True
        return False
