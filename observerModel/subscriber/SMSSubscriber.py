# -*- coding: utf-8 -*-
# @Time    : 2021/10/8 22:17
# @Author  : ZhaoXiangPeng
# @File    : SMSSubscriber.py

from . import Monitor


class SMSSubscriber(Monitor):
    def __init__(self, observer):
        self._observer = observer
        self._observer.register(self)

    def update(self):
        print(f'[{type(self).__name__}]', self._observer.getNews())

