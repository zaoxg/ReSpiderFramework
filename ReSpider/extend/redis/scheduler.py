import ReSpider.setting as setting
from ReSpider.core.scheduler import Scheduler
from .spider import RedisSpider
from ReSpider.utils.make_class import make_req_from_json
import redis
import json


class RedisScheduler(Scheduler):
    name = 'redis scheduler'

    def __init__(self, spider=None, **kwargs):
        super().__init__(spider, **kwargs)
        self.spider = spider

    @classmethod
    def from_settings(cls, spider, **kwargs):
        tag_name = spider.name or spider.__class__.name or spider.__class__.__name__
        cls.queue = setting.REDIS_TASK_QUEUE or f'{tag_name}:scheduler'
        cls.df = setting.REDIS_DUPE_FILTERS or f'{tag_name}:dupefilter'
        cls.error_queue = setting.FAILED_TASK_QUEUE or f'{tag_name}:scheduler:error'
        cls.redis_key = None
        if isinstance(spider, RedisSpider):
            # self._get = self._get_other
            cls.redis_key = spider.redis_key
        return cls(spider, **kwargs)

    def open_spider(self):
        self._pool = redis.ConnectionPool(host=setting.REDIS_HOST or '127.0.0.1',
                                          port=setting.REDIS_PORT or 6379,
                                          password=setting.REDIS_PASSWORD or None,
                                          db=setting.REDIS_DB or 0)
        self._r = redis.Redis(connection_pool=self._pool)

    def __len__(self):
        return self._r.llen(self.queue)

    def enqueue_request(self, request):
        # Todo 理应自动处理优先级且func <verify_priority>干的事太多了
        if request.del_fp:
            self.logger.info('del fingerprint. <%s>' % request.fingerprint)
            self._srem(request.fingerprint)  # 删除指纹
            if setting.SAVE_FAILED_TASK:
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
        arg = self._r.rpush(keys,
                            json.dumps(request.to_dict, ensure_ascii=False))
        return arg

    def _lpush(self, request):
        # 根据优先级判断，0从左边插入
        arg = self._r.lpush(self.queue,
                            json.dumps(request.to_dict, ensure_ascii=False))
        return arg

    def _get(self):
        request = self._r.lpop(self.queue)
        if request is not None:
            request = make_req_from_json(request)
            return request
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
