# -*- coding: utf-8 -*-
# @Time    : 2021/8/31 10:42
# @Author  : ZhaoXiangPeng
# @File    : template_spider.py

import ReSpider
import sys
import os
sys.path.append(os.getcwd().replace('\\spiders', '').rsplit('\\', maxsplit=1)[0])


class TemplateSpider(ReSpider.Spider):
    __custom_setting__ = {}

    name = 'template_spider'
    start_urls = []

    def start_requests(self):
        pass

    def parse(self, response):
        pass


if __name__ == '__main__':
    TemplateSpider().start()
