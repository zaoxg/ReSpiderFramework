from ReSpider.core.spiders import Crawler
from ...extend import SettingLoader


class RedisSpider(Crawler):
    """
    redis spider
    实现一个函数用来解析队列的任务
    """
    name = 'redis_spider'
    redis_key = None
    settings = SettingLoader.from_crawler()

    def __init__(self, redis_key: str = None, **kwargs):
        super().__init__()
        self.settings.update(SCHEDULER='ReSpider.extend.redis.scheduler.RedisScheduler')
        self.settings.update(ALWAYS_RUNNING=True)
        self.__dict__.update(**kwargs)
        if redis_key is None:
            raise AttributeError("Init Error")
        self.redis_key = redis_key

    def make_request(self, **kwargs):
        """
        如果使用这个Spider,
        意味着将持续运行,
        从queue中取出的不一定是Request,
        所以需要重写这个function,
        来实现自己想要的Request
        """
        raise NotImplementedError

    def start_requests(self):
        pass

    def parse(self, response):
        pass
