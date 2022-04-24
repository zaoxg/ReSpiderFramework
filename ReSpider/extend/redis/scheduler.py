import json
from .spider import RedisSpider
import ReSpider.setting as setting
from ReSpider.extend.misc import load_object
from ReSpider.core.scheduler import Scheduler
import ReSpider.utils.make_class as make_class
from ReSpider.db.redisdb import RedisDB


class RedisScheduler(Scheduler):
    name = 'redis scheduler'

    def __init__(self, spider,
                 dupefilter=None, tqcls=None,
                 server=None,
                 task_queue=None, failed_queue=None, df_key=None, **kwargs):
        super().__init__(spider, **kwargs)
        self.spider = spider
        self.server = server
        self.tqcls = tqcls
        self.df = dupefilter
        self.task_queue = task_queue
        self.failed_queue = failed_queue
        self.df_key = df_key

    @classmethod
    def from_settings(cls, spider, **kwargs):
        tag_name = spider.redis_key or spider.name

        server = RedisDB
        dupefilter_obj = load_object(setting.DUPEFILTER)

        task_queue_key = setting.REDIS_TASK_QUEUE % {'redis_key': tag_name}
        dupefilter_key = setting.REDIS_DUPE_FILTERS % {'redis_key': tag_name}
        failed_queue_key = setting.FAILED_TASK_QUEUE % {'redis_key': tag_name}

        cls.redis_key = None

        if isinstance(spider, RedisSpider):
            # self._get = self._get_other
            cls.redis_key = spider.redis_key
        return cls(spider, dupefilter=dupefilter_obj, server=server,
                   task_queue=task_queue_key, failed_queue=failed_queue_key, df_key=dupefilter_key, **kwargs)

    def open_spider(self):
        self.server = self.server()
        self.df = self.df.from_settings(server=self.server, key=self.df_key)

    def __len__(self):
        return self.server.llen(self.task_queue)

    def enqueue_request(self, request):
        # Todo 理应自动处理优先级且func <verify_priority>干的事太多了
        if request.del_fp:
            self.logger.info('del fingerprint. <%s>' % request.fingerprint)
            self._srem(request.fingerprint)  # 删除指纹
            if setting.SAVE_FAILED_TASK:
                self.server.rpush(request, key=self.failed_queue)
            return request
        if request.do_filter and self.df.verify_fingerprint(request):
            return False
        self.verify_priority(request)
        return True

    async def next_request(self):
        try:
            request = self._get()
            if request is None:
                request = self._get_other()
        except Exception as e:
            self.logger.error('Next request error: %s' % e, exc_info=True)
        else:
            return request

    def has_pending_requests(self):
        return self.__len__() > 0

    def _rpush(self, request, key=None):
        if key is None:
            key = self.task_queue
        arg = self.server.rpush(key,
                                json.dumps(request.to_dict, ensure_ascii=False))
        return arg

    def _lpush(self, request):
        # 根据优先级判断，0从左边插入
        arg = self.server.lpush(self.task_queue,
                                json.dumps(request.to_dict, ensure_ascii=False))
        return arg

    def _get(self):
        request = self.server.lpop(self.task_queue)
        if request is not None:
            request = make_class.make_req_from_json(request)
            return request
        return None

    def _get_other(self):
        request = self.server.lpop(self.redis_key) if self.redis_key else None
        if request is not None:
            return self.spider.make_request(request)
        return None

    def _srem(self, fp):
        # 从集合删除一个元素
        self.server.srem(self.df, fp)

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
