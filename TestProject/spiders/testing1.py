# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 17:12
# @Author  : ZhaoXiangPeng
# @File    : testing1.py

# import sys
# import os
# sys.path.append(os.getcwd().replace('\\spiders', '').rsplit('\\', maxsplit=1)[0])
import json
import ReSpider
from ReSpider import item


class Testing1(ReSpider.Spider):
    # name = 'testing_1'

    __custom_setting__ = {
        'a': 1,
        'LOG_TO_FILE': True
    }

    def start_requests(self):
        req = ReSpider.Request(
            # url='https://blog.csdn.net/babybin/article/details/111624905',
            url='http://127.0.0.1:8000/',
            # priority=0,
            do_filter=False,
            callback=self.parse
        )
        yield req

    def parse(self, response):
        # yield ReSpider.Request(
        #     url='https://blog.csdn.net/babybin/article/details/111624905',
        #     callback=self.parse2
        # )
        # yield item.MysqlItem({'name': 'baidu', 'url': 'www.baidu.com'}, table='website')
        # print(response.headers)
        self.logger.info(response)
        # self.logger.warning(response.cookiejar)
        # yield response.cookiejar
        # self.logger.info(response.headers)

    async def parse2(self, response):
        self.logger.warning(response.cookies)
        file_item1 = item.FileItem(json.dumps(response.cookiejar), filename='testing1', filetype='json')
        yield file_item1
        # self.logger.warning(response.text)
        file_item = item.FileItem(response.text, filename='testing1', filetype='html')
        yield file_item


if __name__ == '__main__':
    testing_1 = Testing1(TASK_LIMIT=100)
    testing_1.start()
