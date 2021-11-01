# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 9:20
# @Author  : ZhaoXiangPeng
# @File    : scheduler.py


import ReSpider


class SchedulerTest(ReSpider.Spider):
    name = 'scheduler_test'

    def __init__(self):
        super().__init__()
        self.settings.update(SCHEDULER='ReSpider.extend.redis.scheduler.RedisScheduler')

    def start_requests(self):
        req = ReSpider.Request(
            url='https://blog.csdn.net/babybin/article/details/111624905',
            # priority=0,
            callback=self.parse
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

    def parse(self, response):
        # print(response.headers)
        # self.logger.info(response.cookies)
        self.logger.warning(response.cookiejar)
        # self.logger.info(response.headers)


if __name__ == '__main__':
    sp_test = SchedulerTest()
    sp_test.start()
