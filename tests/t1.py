# -*- coding: utf-8 -*-
# @Time    : 2021/9/13 16:15
# @Author  : ZhaoXiangPeng
# @File    : t1.py

import time
import queue


class Task:
    running: bool = False
    __status: str = None

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, val):
        self.__status = val

    @property
    def task_await(self):
        return None

    @task_await.setter
    def task_await(self, val):
        if val:
            self.status = 'pending'


class EventLoop:
    __loop = queue.Queue()

    def create_task(self, task):
        self.__loop.put(task)

    def run(self):
        while self.__loop.empty():
            task = self.__loop.get()
            task()


class ChildTask(Task):

    def __call__(self, *args, **kwargs):
        self.running = True
        print('%s, do something...' % int(time.time()))
        self.task_await = True
        time.sleep(1)


if __name__ == '__main__':
    loop = EventLoop()
    for i in range(3):
        loop.create_task(ChildTask()())
    loop.run()
