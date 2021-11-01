# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 10:20
# @Author  : ZhaoXiangPeng
# @File    : testing4.py
import json

import ReSpider
from ReSpider import item
from parsel import Selector
import json


class Testing5(ReSpider.RedisSpider):

    name = 'testing5'

    def __init__(self, redis_key):
        super().__init__(redis_key=redis_key)

    def make_request(self, a):
        req = ReSpider.Request(
            url='https://www.baidu.com/s',
            params=json.loads(a)
        )
        return req

    async def parse(self, response):
        print(response)
        yield ReSpider.Request(
            url='https://www.mi.com/',
            callback=self.parse2
        )

    def parse2(self, response):
        meta = response.meta
        # self.logger.debug(meta)
        resp_text = response.text
        return
        html = json.loads(resp_text)
        selector = Selector(html)
        dizhi = selector.xpath('//*[@id="company-top"]/div/div/span[2]/small/text()[2]').extract_first()
        jianjie = selector.xpath('//*[@id="divwebsite"]/section/div[3]/div/div[1]/div/div/div[3]/span[2]/text()').extract_first()
        self.logger.debug('%s\n%s' % (dizhi, jianjie))
        table_tr_nodes = selector.xpath('//*[@id="divCominfo"]/table/tr')
        self.logger.info(table_tr_nodes)
        it = {}
        for tr_node in table_tr_nodes:
            k = tr_node.xpath('./td[@class="ma_bluebg ma_left"]/text()')
            v = tr_node.xpath('./td[@class="ma_left"]/text()')
            print(zip(k, v))


if __name__ == '__main__':
    # from ReSpider.utils import urlDecode
    #
    # print(urlDecode('country=&city=&pid=Kz6qgBMyXjVL0v1MqAvpAblEeaPNOwR8&vcnt=1&page=1'))
    Testing5(redis_key='zhaoxp').start()
