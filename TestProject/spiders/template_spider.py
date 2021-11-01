# -*- coding: utf-8 -*-
# @Time    : 2021/8/31 10:42
# @Author  : ZhaoXiangPeng
# @File    : template_spider.py

import ReSpider


class TemplateSpider(ReSpider.Spider):

    name = 'template_spider'
    start_urls = []

    def __init__(self):
        super().__init__()

    def start_requests(self):
        pass

    def parse(self, response):
        pass
