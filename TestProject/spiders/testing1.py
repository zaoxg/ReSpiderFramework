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
            url='https://blog.csdn.net/babybin/article/details/111624905',
            # priority=0,
            callback=self.parse2
        )
        yield req
        # for url in self.start_urls:
        #     yield ReSpider.Request(
        #         url=url,
        #         method='GET',
        #         allow_redirects=False,
        #         do_filter=True
        #     )
        # yield ReSpider.Request(
        #     url='https://blog.csdn.net/babybin/article/details/111624905',
        #     priority=0,
        #     callback=self.parse
        # )
        # if self.start_urls:
        #     for url in self.start_urls:
        #         yield ReSpider.Request(url=url)

    async def parse(self, response):
        # print(response.headers)
        # self.logger.info(response.cookies)
        self.logger.warning(response.cookiejar)
        yield response.cookiejar
        # self.logger.info(response.headers)

    async def parse2(self, response):
        self.logger.warning(response.cookies)
        file_item1 = item.FileItem(json.dumps(response.cookiejar), filename='testing1', filetype='json')
        yield file_item1
        # self.logger.warning(response.text)
        file_item = item.FileItem(response.text, filename='testing1', filetype='html')
        yield file_item


if __name__ == '__main__':
    testing_1 = Testing1()
    testing_1.start()
