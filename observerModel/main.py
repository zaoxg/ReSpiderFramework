# -*- coding: utf-8 -*-
# @Time    : 2021/10/8 22:20
# @Author  : ZhaoXiangPeng
# @File    : main.py

from observerModel.observer import Observer
from observerModel.subscriber.PhoneSubscriber import PhoneSubscriber
from observerModel.subscriber.EmailSubscriber import EmailSubscriber
from observerModel.subscriber.SMSSubscriber import SMSSubscriber


def A_B(a, b):
    return a + b


class Engine:
    observer = Observer()

    def __init__(self):
        self.phone = PhoneSubscriber(self.observer)
        self.email = EmailSubscriber(self.observer)
        self.sms = SMSSubscriber(self.observer)
        self.observer.add_func(A_B)

    def step1(self):
        self.observer.notify()

    def step2(self):
        print(self.phone.A_B(5, 4))
        print(self.email.A_B(9, 4))
        print(self.sms.A_B(5, 7))


if __name__ == '__main__':
    e = Engine()
    print(e.observer.observers())
    e.observer.latestNews = 'get'
    e.step1()
    e.step2()
