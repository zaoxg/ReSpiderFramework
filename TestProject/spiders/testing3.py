# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 9:56
# @Author  : ZhaoXiangPeng
# @File    : testing3.py
# ssl指纹测试


import ReSpider


class Testing3(ReSpider.Spider):
    __custom_setting__ = {'TASK_LIMIT': 1, 'LOG_LEVEL_CONSOLE': 'INFO', 'DOWNLOADER_MIDDLEWARES': {}, 'LOG_TO_CONSOLE': True,
                          'SSL_FINGERPRINT': False}
    name = 'testing3'
    # start_urls = ['https://ja3er.com/json'] * 3
    # start_urls = ['https://www.baidu.com/'] * 100
    start_urls = ['http://127.0.0.1:8000/'] * 100
    # start_urls = ['https://ja3er.com/json'] * 10

    def parse(self, response):
        self.logger.info(response)


if __name__ == '__main__':
    Testing3().start()
