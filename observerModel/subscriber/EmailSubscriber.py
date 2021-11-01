# -*- coding: utf-8 -*-
# @Time    : 2021/10/8 22:19
# @Author  : ZhaoXiangPeng
# @File    : EmailSubscriber.py

from . import Monitor


class EmailSubscriber(Monitor):
    def __init__(self, observer):
        self._observer = observer
        self._observer.register(self)

    def update(self):
        # time.sleep(random.random())
        print(f'[{type(self).__name__}]', self._observer.getNews())
