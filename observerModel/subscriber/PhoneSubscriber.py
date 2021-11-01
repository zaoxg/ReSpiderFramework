# -*- coding: utf-8 -*-
# @Time    : 2021/10/8 22:19
# @Author  : ZhaoXiangPeng
# @File    : PhoneSubscriber.py

from . import Monitor


class PhoneSubscriber(Monitor):
    def __init__(self, observer):
        self._observer = observer
        self._observer.register(self)

    def update(self):
        print(f'[{type(self).__name__}]', self._observer.getNews())
