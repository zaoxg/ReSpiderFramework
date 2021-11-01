# -*- coding: utf-8 -*-
# @Time    : 2021/8/21 22:03
# @Author  : ZhaoXiangPeng
# @File    : observer.py
import asyncio
import time
import random


class Observer:
    _task_count = 0
    __observers = []
    loop = asyncio.get_event_loop()
    __latestNews = None

    # def __init__(self):
    #     self._task_count = 0
    #     self.__observers = []
    #     self.loop = asyncio.get_event_loop()

    def register(self, obj):
        self.__observers.append(obj)

    def add_func(self, func):
        func_name = func.__qualname__
        print(func_name)
        for observer in self.__observers:
            observer.__setattr__(func_name, func)

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
            self.notify()

    def getNews(self):
        return time.time().__str__() + " | Got News: " + self.__latestNews

    def observers(self):
        return [type(x).__name__ for x in self.__observers]

    def notify(self):
        for observer in self.__observers:
            observer.update()
            # time.sleep(random.random())


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
    for sub in [SMSSubscriber, EmailSubscriber, PhoneSubscriber]:
        sub(obs)
    print(obs.observers())
    for i in range(200):
        obs.latestNews = '({})不要回答! 不要回答! 不要回答!'.format(i)
        # time.sleep(random.random())
        # obs.latestNews = '收到请回答! 收到请回答! 收到请回答!'
        # obs.latestNews = '不要回答! 不要回答! 不要回答!'
    # obs.notify()
