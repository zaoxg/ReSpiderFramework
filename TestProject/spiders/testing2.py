# -*- coding: utf-8 -*-
# @Time    : 2021/8/31 11:11
# @Author  : ZhaoXiangPeng
# @File    : testing2.py

import ReSpider


class Testing2(ReSpider.Spider):
    __custom_setting__ = {
        'DOWNLOADER_MIDDLEWARES': {
            'ReSpider.extend.puppeteer.downloadmiddleware.PuppeteerMiddleware': 6
        }
    }
    # name = 'testing_2'
    """
    需要加载浏览器相关配置
    """
    # start_urls = ['http://qikan.cqvip.com/Qikan/Article/Detail?id=7103439850',
    #               'http://qikan.cqvip.com/Qikan/Article/Detail?id=7102760064',
    #               'http://qikan.cqvip.com/Qikan/Article/Detail?id=7101531000',
    #               'http://qikan.cqvip.com/Qikan/Article/Detail?id=7103385685']

    start_urls = ['http://127.0.0.1:8000/'] * 10

    # def __init__(self):
    #     super().__init__()
    #     self.settings['DOWNLOADER_MIDDLEWARES'].update({'ReSpider.extend.puppeteer.downloadmiddleware.PuppeteerMiddleware': 6})

    def start_requests(self):
        for url in self.start_urls:
            yield ReSpider.PuppeteerRequest(
                url=url,
                wait_until='networkidle2',
            )

    def parse(self, response):
        # self.logger.warning(response.cookies)
        print(response.text)
        cookiejar = response.cookies
        cookies = []
        for c in cookiejar:
            cookies.append(f'{c["name"]}={c["value"]}')
        cookie = '; '.join(cookies)
        self.logger.info('parse cookie -> %s' % cookie)


if __name__ == '__main__':
    Testing2().start()
