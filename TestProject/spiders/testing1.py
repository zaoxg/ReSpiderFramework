# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 17:12
# @Author  : ZhaoXiangPeng
# @File    : testing1.py

import sys
import os
sys.path.append(os.getcwd().replace('\\spiders', '').rsplit('\\', maxsplit=1)[0])
import json
import ReSpider
from ReSpider import item


class Testing1(ReSpider.Spider):
    name = 'testing_1'

    def __init__(self):
        super().__init__()
        # self.settings.get('DOWNLOADER_MIDDLEWARES', {}).update(
        #     {'ReSpider.extend.puppeteer.downloadmiddleware.PuppeteerMiddleware': 6})
        # self.settings.update(SCHEDULER='ReSpider.extend.redis.scheduler.RedisScheduler')
        # self.settings.update(SCHEDULER='ReSpider.core.scheduler.Scheduler')
        # self.settings.update(STREAM_HANDLER_LEVEL='INFO')
        print(self.settings)

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
        file_item1 = item.FileItem(filename='testing1', filetype='json')
        file_item1['source'] = json.dumps(response.cookiejar)
        yield file_item1
        # self.logger.warning(response.text)
        file_item = item.FileItem(filename='testing1', filetype='html')
        file_item['source'] = response.text
        yield file_item


if __name__ == '__main__':
    testing_1 = Testing1()
    testing_1.start()
