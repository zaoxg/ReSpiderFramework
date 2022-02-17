# -*- coding: utf-8 -*-
# @Time    : 2021/8/21 22:03
# @Author  : ZhaoXiangPeng
# @File    : observer.py

import math
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
ORIGINAL_DOWNLOAD_DELAY = setting.DOWNLOAD_DELAY  # 存一下原始的值
ORIGINAL_TASK_LIMIT = setting.CONCURRENT_REQUESTS = setting.TASK_LIMIT
OPERATION_TIME = 20  # 操作间隔时间


class Observer(LogMixin):
    loop = asyncio.get_event_loop()
    _task_count = 0
    __observers = {}  # 主要的被观察对象 scheduler, middleware manager(download, pipeline)
    __pipelines = {}  # 被观察的 pipeline obj 列表
    __middlewares = {}  # 被观察的 middleware obj 列表
    __SIGNAL_STATUS = None

    __ScheduledTask__ = {}

    __requestCount = 0
    __requestFailCount = 0
    __intervalCount = 0
    __intervalFailCount = 0

    __latestMessage = None

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
        elif self.__SIGNAL_STATUS == 'STOP':
            for scheduled_task, task_obj in self._scheduled_task().items():
                task_obj.cancel()  # 取消定时任务
            for _observer in self.__observers.keys():
                self.__observers[_observer].close_spider()
            self.logger.info('send request <%d> total, fail request <%d> total.' % (self.request_count, self.request_count_fail))
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
        interval_time = setting.REQUEST_COUNT_INTERVAL_TIME or REQUEST_COUNT_INTERVAL_TIME
        self.logger.info('last %d minutes, send request <%s> total, fail <%s> total.' %
                         (interval_time/60, self.__intervalCount, self.__intervalFailCount))
        self.__intervalCount, self.__intervalFailCount = 0, 0  # 通知后重置请求和失败次数
        loop.call_later(interval_time, self.callback, loop)

    def request_count_init(self, loop):
        self.logger.debug('request count service init.')
        interval_time = setting.REQUEST_COUNT_INTERVAL_TIME or REQUEST_COUNT_INTERVAL_TIME
        loop.call_later(interval_time, self.callback, loop)

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
    def latest_message(self):
        return self.__latestMessage

    @latest_message.setter
    def latest_message(self, value):
        def reset_news():
            self.__latestMessage = None
        if self.__latestMessage != value:
            self.__latestMessage = value
            self._set_scheduled(
                'RESET_MESSAGE',
                self.loop.call_later(OPERATION_TIME, reset_news)  # 指定时间后重新设置值
            )
            self.notify(value)

    def getMsg(self):
        return time.time().__str__() + " | Got Massage: " + self.__latestMessage

    def observers(self):
        return [x.__name__ for x in self.__observers]

    def set_concurrent(self, val: int = 2, limit: int = None):
        def restore(t):
            setting.CONCURRENT_REQUESTS = setting.TASK_LIMIT = t
            self.logger.warning('恢复请求并发, 恢复后配置为: 并发: %s' % setting.TASK_LIMIT)
        if self._get_scheduled('TASK_LIMIT_TASK'):
            # 如果已经设置则取消, 等待重新设置
            self._get_scheduled('TASK_LIMIT_TASK').cancel()  # 取消执行
        else:
            setting.CONCURRENT_REQUESTS = setting.TASK_LIMIT = limit or math.ceil(setting.TASK_LIMIT/val)
            self.logger.warning('限制请求频次, 修改后配置为: 并发: %s' % setting.TASK_LIMIT)
        # 重新设置
        self._set_scheduled(
            'TASK_LIMIT_TASK',
            self.loop.call_later(30 * 60, restore, ORIGINAL_DOWNLOAD_DELAY)
        )  # 30分钟后还原

    def set_delay(self, delay: int = 1):
        def restore(d):
            setting.DOWNLOAD_DELAY = d
            self.logger.warning('恢复请求延迟, 恢复后配置为: 延迟: %s' % setting.DOWNLOAD_DELAY)
        if self._get_scheduled('DOWNLOAD_DELAY_TASK'):
            # 如果已经设置则取消, 等待重新设置
            self._get_scheduled('DOWNLOAD_DELAY_TASK').cancel()  # 取消执行
        else:
            setting.DOWNLOAD_DELAY = delay
            self.logger.warning('修改延迟, 修改后配置为: 延迟: %s' % setting.DOWNLOAD_DELAY)
        # 重新设置
        self._set_scheduled(
            'DOWNLOAD_DELAY_TASK',
            self.loop.call_later(30 * 60, restore, ORIGINAL_DOWNLOAD_DELAY)
        )  # 30分钟后还原

    def _scheduled_task(self):
        return self.__ScheduledTask__

    def _set_scheduled(self, task_name, task_obj):
        # 存储定时任务
        self.__ScheduledTask__.update({task_name: task_obj})

    def _get_scheduled(self, task_name):
        return self.__ScheduledTask__.get(task_name)

    def execute_func(self, func, **kwargs):
        # Todo 锁一下, 防止重复操作
        func(**kwargs)

    def notify(self, msg):
        self.logger.warning('RNM this local has trouble, is <%s>' % msg)


if __name__ == '__main__':
    obs = Observer()
