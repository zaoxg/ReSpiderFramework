from ...core.scheduler import Scheduler
import redis
import pickle
from .spider import RedisSpider


class RedisScheduler(Scheduler):
    def __init__(self, spider=None, **kwargs):
        super().__init__(spider, **kwargs)
        tag_name = spider.name or spider.__class__.name or spider.__class__.__name__
        self.settings = spider.settings
        self._pool = redis.ConnectionPool(host=self.settings.get('REDIS_HOST', '127.0.0.1'),
                                          port=self.settings.get('REDIS_PORT', 6379),
                                          password=self.settings.get('REDIS_PASSWORD', None),
                                          db=self.settings.get('REDIS_DB', 0))
        self._r = redis.Redis(connection_pool=self._pool)
        self.queue = f'{tag_name}:scheduler'
        self.df = f'{tag_name}:dupefilter'
        self.error_queue = f'{tag_name}:scheduler:error'
        self.redis_key = None
        if isinstance(spider, RedisSpider):
            # self._get = self._get_other
            self.redis_key = spider.redis_key

    @classmethod
    def open_spider(cls, spider=None):
        return cls(spider)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        return cls(spider, **kwargs)

    def __len__(self):
        return self._r.llen(self.queue)

    def enqueue_request(self, request):
        # 优先级(循环太多了)
        if request.meta is not None and request.meta.get('del_fp', False):
            self.logger.info('DEL FINGERPRINT...')
            self._srem(request.fingerprint)  # 删除指纹
            self._rpush(request, keys=self.error_queue)
            return request
        if request.do_filter:
            if self.verify_fingerprint(request):
                self.verify_priority(request)
        else:
            self.verify_priority(request)
        return request

    async def next_request(self):
        try:
            request = self._get()
            if request is None:
                request = self._get_other()
        except Exception as e:
            self.logger.error('[NEXT REQUEST ERROR] %s' % e, exc_info=True)
        else:
            return request

    def has_pending_requests(self):
        return self._r.llen(self.queue) > 0

    def _rpush(self, request, keys=None):
        if keys is None:
            keys = self.queue
        arg = self._r.rpush(keys, pickle.dumps(request))
        return arg

    def _lpush(self, request):
        # 根据优先级判断，0从左边插入
        arg = self._r.lpush(self.queue, pickle.dumps(request))
        return arg

    def _get(self):
        request = self._r.lpop(self.queue)
        if request is not None:
            return pickle.loads(request)
        return None

    def _get_other(self):
        request = self._r.lpop(self.redis_key) if self.redis_key else None
        if request is not None:
            return self.spider.make_request(request)
        return None

    def _srem(self, fp):
        # 从集合删除一个元素
        self._r.srem(self.df, fp)

    def verify_priority(self, request):
        """
        校验优先级
        :param request:
        :return:
        """
        # self.logger.debug(pickle.dumps(request))
        if request.priority < 1:
            res = self._lpush(request)
        else:
            res = self._rpush(request)
        return res

    def verify_fingerprint(self, request):
        """
        :return:
        """
        fp = request.fingerprint
        if self._r.sismember(self.df, fp) is False:
            self._r.sadd(self.df, fp)
            return True
        return False
