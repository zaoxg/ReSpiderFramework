# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 9:42
# @Author  : ZhaoXiangPeng
# @File    : setting_logger.py


from ReSpider.testing.log_test import logger


class A:
    logger.debug('A')

    def func1(self):
        logger.debug('func1')


a = A()
a.func1()
