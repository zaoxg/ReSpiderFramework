# -*- coding: utf-8 -*-
# @Time    : 2021/8/21 22:03
# @Author  : ZhaoXiangPeng
# @File    : observer.py


import asyncio
import time
from ReSpider.extend import LogMixin
import ReSpider.setting as setting

# 被观察者列表
# 	调度器
# 	下载器
# 		DownloaderMiddlewareManager
# 	pipelineManager
#
# 启动方式
# 	3个主要被观察者的from_crawler执行后加载进被观察者列表
# 	当调度器里有任务时启动open_spider进行连接数据库等操作
#
# 观察者要做什么
# 1. 控制pipeline和middleware的开关
# 	open_spider 和 close_spider
# 	middlewareManager需要实现以上两个方法
# 	middlewareManager控制pipelines和middlewares的开启和关闭


__all__ = [
    'Observer'
]

REQUEST_COUNT_INTERVAL_TIME = 120  # 请求统计通知间隔时间


class Observer(LogMixin):
    loop = asyncio.get_event_loop()
    _task_count = 0
    __observers = {}  # 主要的被观察对象 scheduler, middleware manager(download, pipeline)
    __pipelines = {}  # 被观察的 pipeline obj 列表
    __middlewares = {}  # 被观察的 middleware obj 列表
    __SIGNAL_STATUS = None

    __requestCount = 0
    __requestFailCount = 0
    __intervalCount = 0
    __intervalFailCount = 0

    __latestNews = None

    def register(self, obj, default=None):
        self.logger.debug('<%s> register in observer.' % obj.__class__.__name__)
        if default is None:
            self.__observers.update({obj.__class__.__name__: obj})
        elif default == 'pipeline':
            self.__pipelines.update({obj.__class__.__name__: obj})
        elif default == 'middleware':
            self.__middlewares.update({obj.__class__.__name__: obj})

    @property
    def engine_status(self):
        return self.__SIGNAL_STATUS

    @engine_status.setter
    def engine_status(self, value):
        self.__SIGNAL_STATUS = value
        if self.__SIGNAL_STATUS == 'START':
            for _observer in self.__observers.keys():
                self.__observers[_observer].open_spider()
            # Todo
            self.loop.call_soon(self.request_count_init, self.loop)
            # self.loop.call_later(1, callback, self.loop)
        elif self.__SIGNAL_STATUS == 'STOP':
            for _observer in self.__observers.keys():
                self.__observers[_observer].close_spider()
            self.logger.info('send request <%d> times total, fail request <%d> times total' % (self.request_count, self.request_count_fail))
        else:
            pass

    @property
    def task_count(self):
        return self._task_count

    @task_count.setter
    def task_count(self, value):
        self._task_count = value
        if self._task_count < 1:
            return
        elif self._task_count:
            for _observer in self.__observers:
                _observer.open_spider()

    @property
    def request_count(self):
        return self.__requestCount

    @request_count.setter
    def request_count(self, val: int = 1):
        self.__intervalCount += val  # 阶段请求 +1
        self.__requestCount += val

    @property
    def request_count_fail(self):
        return self.__requestFailCount

    @request_count_fail.setter
    def request_count_fail(self, val: int = 1):
        self.__intervalFailCount += val  # 阶段请求 +1
        self.__requestFailCount += val

    def callback(self, loop=None):
        # print('callback with {0}'.format(time.time()))
        # a = self.fail_count / self.request_count
        self.logger.info('last %d minutes, send request <%s> , fail <%s> .' % (REQUEST_COUNT_INTERVAL_TIME/60, self.__intervalCount, self.__intervalFailCount))
        self.__intervalCount, self.__intervalFailCount = 0, 0  # 通知后重置请求和失败次数
        loop.call_later(REQUEST_COUNT_INTERVAL_TIME, self.callback, loop)

    def request_count_init(self, loop):
        self.logger.debug('request count init.')
        loop.call_later(REQUEST_COUNT_INTERVAL_TIME, self.callback, loop)

    async def app_check(self):
        # 当 task_count 变化时触发
        # 获取当前时间循环里的所有任务
        running_tasks = asyncio.all_tasks(self.loop)
        for running_task in running_tasks:
            print(running_task.get_coro())
            print(running_task.get_name())
            # 一般来讲, 只会有这个一个任务
            if running_task.get_name() != '_next_request':
                # 关闭除 _next_request 的其他任务
                running_task.done()
        for obj in self.__observers:
            pass

    @property
    def latestNews(self):
        return self.__latestNews

    @latestNews.setter
    def latestNews(self, value):
        if self.__latestNews != value:
            self.__latestNews = value
            self.notify(value)

    def getNews(self):
        return time.time().__str__() + " | Got News: " + self.__latestNews

    def observers(self):
        return [type(x).__name__ for x in self.__observers]

    def notify(self, msg):
        self.logger.warning('rnm this local has some little trouble, content is <%s>' % msg)
        # for observer in self.__observers:
        #     observer.open_spider()


class Monitor:
    def update(self):
        pass


class SMSSubscriber(Monitor):
    def __init__(self, observer):
        self._observer = observer
        self._observer.register(self)

    def update(self):
        print(f'[{type(self).__name__}]', self._observer.getNews())


class EmailSubscriber(Monitor):
    def __init__(self, observer):
        self._observer = observer
        self._observer.register(self)

    def update(self):
        # time.sleep(random.random())
        print(f'[{type(self).__name__}]', self._observer.getNews())


class PhoneSubscriber(Monitor):
    def __init__(self, observer):
        self._observer = observer
        self._observer.register(self)

    def update(self):
        print(f'[{type(self).__name__}]', self._observer.getNews())


if __name__ == '__main__':
    obs = Observer()
    obs.latestNews = '收到请回答! 收到请回答! 收到请回答!'
    # for sub in [SMSSubscriber, EmailSubscriber, PhoneSubscriber]:
    #     sub(obs)
    # print(obs.observers())
    # for i in range(200):
    #     obs.latestNews = '({})不要回答! 不要回答! 不要回答!'.format(i)
        # time.sleep(random.random())
        # obs.latestNews = '收到请回答! 收到请回答! 收到请回答!'
        # obs.latestNews = '不要回答! 不要回答! 不要回答!'
    # obs.notify()
