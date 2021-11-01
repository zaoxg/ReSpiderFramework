# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 9:56
# @Author  : ZhaoXiangPeng
# @File    : testing3.py
# ssl指纹测试


import ReSpider


class Testing3(ReSpider.Spider):
    name = 'testing3'
    start_urls = ['https://ja3er.com/json'] * 3

    def __init__(self):
        super().__init__()
        self.settings.update(SSL_FINGERPRINT=True)

    def parse(self, response):
        self.logger.debug(response.json())


if __name__ == '__main__':
    Testing3().start()
