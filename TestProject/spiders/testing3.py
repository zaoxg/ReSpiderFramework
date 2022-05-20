# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 9:56
# @Author  : ZhaoXiangPeng
# @File    : testing3.py
# ssl指纹测试

import time
import ReSpider
from ReSpider import item
from random import randint


class Testing3(ReSpider.Spider):
    __custom_setting__ = {'TASK_LIMIT': 100, 'LOG_LEVEL_CONSOLE': 'DEBUG', 'DOWNLOADER_MIDDLEWARES': {}, 'LOG_TO_CONSOLE': True,
                          'SSL_FINGERPRINT': True}
    name = 'testing3'
    # start_urls = ['https://company.hecrab.com'] * 3
    start_urls = ['https://www.baidu.com/s?ie=UTF-8&wd=site:(neu.edu.cn) "李鸿儒"'] * 3
    # start_urls = ['https://www.baidu.com/'] * 10
    # start_urls = ['http://127.0.0.1:8000/'] * 50
    # start_urls = ['https://ja3er.com/json'] * 2

    # def start_requests(self):
    #     for i in range(50):
    #         yield ReSpider.Request(
    #             url='http://127.0.0.1:8000',
    #             # headers={
    #             #     'Accept-Encoding': 'gzip, deflate, br',
    #             #     'Host': 'www.baidu.com',
    #             #     # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
    #             # },
    #             priority=randint(0, 10),
    #             do_filter=False,
    #         )

    def parse(self, response):
        self.logger.info(response.url)
        print(response.text)
        # data = item.RdsItem(response.json(), key='testing3')
        # # yield data
        # data2 = item.RdsListItem([response.json()], key='testing3')
        # data2.append({'a': '1'})
        # data2.append({'b': '2'})
        # data2.append({'c': '3'})
        # yield data2
        # self.logger.info(response.json())
        # raise IndexError('out of index')
        # yield item.DataItem({'test_id': int(time.time_ns()/1000)}, collection='data_test')


if __name__ == '__main__':
    Testing3(TASK_LIMIT=1,
             redis_key='test3').start()
