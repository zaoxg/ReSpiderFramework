# -*- coding: utf-8 -*-
# @Time    : 2022/8/15 10:31
# @Author  : ZAOXG
# @File    : testing2.py

import ReSpider
from ReSpider.extend.notify.dingtalk import DingTalkNotify


class Testing2(ReSpider.Spider):
    __custom_setting__ = {'SSL_FINGERPRINT': True}

    def start_requests(self):
        req = ReSpider.PuppeteerRequest(
            url='http://epub.cnipa.gov.cn/',
            # url='https://www.bengbu.gov.cn/site/label/8888?IsAjax=1&_=0.15884074755608024&labelName=publicInfoList&siteId=6795621&pageSize=15&pageIndex=2&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=21981&type=4&catId=7225431&title=&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fc1%2Fbengbu%2FpublicInfoList_new2022',
            # url='http://www.jinair.com',
            do_filter=False,
            callback=self.parse
        )
        yield req

    def parse(self, response):
        # DingTalkNotify.info(response.url.__str__())
        self.logger.info(response)
        self.logger.info(response.cookiejar)


if __name__ == '__main__':
    testing_2 = Testing2()
    testing_2.start()
