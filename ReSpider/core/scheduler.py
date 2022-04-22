import asyncio
from asyncio import PriorityQueue
from ReSpider.extend.logger import LogMixin
from ReSpider.extend.misc import load_object
import ReSpider.setting as setting


class Scheduler(LogMixin):
    name = 'scheduler'

    def __init__(self, spider,
                 dupefilter=None,
                 tqcls=None, **kwargs):
        super().__init__(spider)
        self.df = dupefilter
        self.tqcls = tqcls
        self._observer = kwargs.pop('observer', None)
        if self._observer:
            self._observer.register(self)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        return cls.from_settings(spider, **kwargs)

    @classmethod
    def from_settings(cls, spider, **kwargs):
        dupefilter_obj = load_object(setting.DUPEFILTER)
        dupefilter = dupefilter_obj.from_settings()
        return cls(spider, dupefilter=dupefilter, tqcls=PriorityQueue, **kwargs)

    def open_spider(self):
        self.task_queue = self.tqcls()
        self.df.open()

    def close_spider(self):
        pass

    def __len__(self):
        """
        返回队列任务数
        :return:
        """
        return self.task_queue.qsize()

    def enqueue_request(self, request):
        """
        向队列中插入一个请求, 如果需要去重则将指纹加入去重器
        :param request:
        :return: success -> True, failed -> False
        """
        if request.do_filter and self.df.verify_fingerprint(request):
            return False
        self.task_queue.put_nowait(request)
        return True

    async def next_request(self):
        """
        获取下一个请求
        :return:
        """
        try:
            request = self.task_queue.get_nowait()
        except asyncio.queues.QueueEmpty:
            request = None
        return request

    def has_pending_requests(self):
        """
        判断队列中是否有请求
        :return:
        """
        return self.task_queue.qsize() > 0

    def _srem(self, fp):
        # 从集合删除一个元素
        self.df.remove(fp)
