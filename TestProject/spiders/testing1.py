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
            do_filter=True,
            callback=self.parse2
        )
        # request = {'url': 'https://blog.csdn.net/babybin/article/details/111624905', 'method': 'GET', 'headers': {}, 'params': {}, 'data': {}, 'cookies': {}, 'allow_redirects': True, 'encoding': 'utf-8', 'proxy': '', 'timeout': 30, 'meta': None, 'priority': 1, 'fingerprint': '990aa332b9e08ba7557766ebab3f6f9b', '_Request__do_filter': True, 'retry': False, 'retry_times': 0, 'max_retry_times': 5, 'callback': self.parse, 'errback': None}
        # req = ReSpider.Request(**request)
        # self.logger.warning(req)
        # print(req.cat())
        import json
        # print(json.dumps(req.to_dict, ensure_ascii=False))
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
    testing_1 = Testing1(TASK_LIMIT=1)
    testing_1.start()
