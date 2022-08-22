# -*- coding: utf-8 -*-
# @Time    : 2022/8/15 10:31
# @Author  : ZAOXG
# @File    : testing2.py

import ReSpider


class Testing2(ReSpider.Spider):

    def start_requests(self):
        req = ReSpider.PuppeteerRequest(
            url='http://epub.cnipa.gov.cn/',
            do_filter=False,
            callback=self.parse
        )
        yield req

    def parse(self, response):
        self.logger.info(response)


if __name__ == '__main__':
    testing_2 = Testing2()
    testing_2.start()
