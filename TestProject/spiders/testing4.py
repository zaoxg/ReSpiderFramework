# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 10:20
# @Author  : ZhaoXiangPeng
# @File    : testing4.py
import json

import ReSpider
from ReSpider import item
from parsel import Selector


class Testing4(ReSpider.Spider):
    name = 'testing4'

    def __init__(self):
        super().__init__()

    def start_requests(self):
        yield ReSpider.Request(
            url='https://www.webofscience.com/api/wosnx/core/runQuerySearch?SID=7AVlHukiTs3LwR7yZEK',
            method='POST',
            headers={
                'authority': 'www.webofscience.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'x-sec-clge-req-type': 'ajax',
                'accept': 'application/x-ndjson',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                'sec-ch-ua-platform': '"Windows"',
                'content-type': 'text/plain;charset=UTF-8',
                'origin': 'https://www.webofscience.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.webofscience.com/wos/alldb/advanced-search',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cookie': 'bm_sz=150DA218CEACABEF6C40656E4D792C27~YAAQpfEoFz1UOPR7AQAAHN9VGA2bCwYff5mzS0D66jDTubEZcqvrVrYuFqcPD/spakoD9yhIM6/JNdFa7sVVqgp1h6VAPccE0L9Ka0PppJCoJRvrDwLnd+Z2hUvGGIHj3WOizjoG1IM5MphPaI6mArliyVWmExZECR10JIfbMJoyEOpD1qPi7rW5sv1EXQqnEThOxmoS; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; ak_bmsc=C5E876309136BBF150BE7532A813673C~000000000000000000000000000000~YAAQpfEoF0lUOPR7AQAAxAtWGA2vglL9hw/EtMMEGjyPLxWP4/VmIc3NW55khiwjGzoyp/4QFyxC2Uivi2Xg5AdHljQ9wvBoYdHENgKsJ83EdPR6YorkZKL5GDFLgzn+RgCvTRMMPmiZQ6dZA300V+dEiz6uWBCL8KsrYW5nxZLiVaPTtcOpraEEA8DWVRPSdEGpWcO5JvQz9F4NYNPjZ5GsBJD9ez3wvNrH5gEVxBNhzfMI/OjqTDE94RLwpFT8QsT6IYkIwJc3GCs3F81b6tlTDjTOc+qa+RUIYfeCc7IGJozaxgfMbjfVGyQ1nmRdlpnYxWkFYxmhB4o/gxeEVNivyAHkGp/zxXOUoftAz5YoK8m7/V9/tocDdDF3la1Ki9c=; _sp_ses.4e8e=*; RT="z=1&dm=www.webofscience.com&si=1f4077cd-67e3-4ab6-bc03-abb40e5eb5a4&ss=ktyhvy84&sl=1&tt=3to&bcn=%2F%2F684d0d39.akstat.io%2F"; bm_sv=457B0375413C51D18D909CC8853344A8~dsSiz/Bms2UXYEN977SpskPrJWxHnVxJd9mHYXgZ+eX8ilDK+smomXx6bic+j+3uBfQQkrTmkTn59bnM73ekAy81mPx2r8nmoyq1x2MzTjMgxig1yndzMhf0njKRliEls3jX32VxxiIWrhap+ylzcgn+5Gr67f9PNRdZ+eHFMPo=; _abck=5B0CA6B243222399272CA6D3856F34E4~0~YAAQxfEoF4zCpsp7AQAAGHFeGAarcFU23YlUikCoUJ9NByJPzPTond3vQkY+d342zkGuVSSiJml2tkD4V8JTUimGp75yprAL0ccE5JtXQOHPSAC6O+YWJ36BlzWMXGQ3+/1XXiDc9VCexIRGzQTAvPZ5fdwYn5ECZefxLEocBGHPdZDGoLromfurjU4ITCOQtyYqFrERAayOQNBp4Bao1DmxGCmWEESgYhCd60M1E/rTuIh0OU9aVKXGOB5Al5xshipXNVVnUP2T1cS6uWx1+2yo1NX5nqfghG44ZUkwXGqLPb6zygCHku2Sow3/kzehM9NKKOpNi8h0HVEUuQg5XfBr54JZEmikpJh4U8QB8AtodYFRNCVAJ1lfFz7KLsd+Y6dfUkdpQ2G+ialHJDUX9DxASOpWCAzeE2BA8Vyx~-1~-1~-1; _sp_id.4e8e=ec2a2389-70ad-48fa-9587-e61766dcb5d5.1632495866.1.1632496480.1632495866.928808cd-01e6-4298-bb25-c6bad81ff314; bm_sv=457B0375413C51D18D909CC8853344A8~dsSiz/Bms2UXYEN977SpskPrJWxHnVxJd9mHYXgZ+eX8ilDK+smomXx6bic+j+3uBfQQkrTmkTn59bnM73ekAy81mPx2r8nmoyq1x2MzTjM3zVMRBTx8RUYmvB0sXLt+xQrpjtKzTkCvhg9bRWCUL7Bo2/LGhwRdAxWv4Ca9alE=; _abck=5B0CA6B243222399272CA6D3856F34E4~-1~YAAQxfEoF2HFpsp7AQAAJL1gGAaC+4BEC1pKTB+SKtWS7pnE+mjJQOhlSlFcbORsuDwhdL8H/nnZvCa+Ksjp3/w2a3cAnFFsbcWs+LYqHXqlbXRz5JB86QVgs+ZmbxDWnsCpopuFdGRpRVRoTYtqW304bXqjth7EhCiUbnL84ySjnV0N81V/NBHFEMFuetvAvaJkKshAxeWgJzsUvGQiamsknN6Rbi1jEjje0fKLZn3UNr8HhTiZEdCSM8pz8d+7Yxf2POD4Y2VTDqfOxZeslRcET9XAgX/13FpKHPGEiDeZyhP7JJOXqJskeXokwm/kOe5E0vsFrW96pyABonuUHPjeJi4XMIbSWK6tBvRVab1ENNdjHbX6ed4DAo/Wa21OfK5NuGzV5gBR1S+oKzJ480ReJnmtE2V0lJ64DhOR~0~-1~-1; sec_cpt=E9D6293C93BA21028D6E354245A3A5D9~1~YAAQxfEoF2LFpsp7AQAAJL1gGAVQdN8zTbdMsl8wny9fIH0xnWOIGvKgWLSlMFaorRBVcgSjJiav2A+mVcSY+zDtEco4IF+M2OqKw8yLoGhdxfcA1W+IApqkAjtsIOY5ABksC+OR1Y+8QK2L4oF2ONVg/7db2BY91b34f36CgEy2fIzXN5k5KWwOPuYq0O1U7yFrTl4TxWOrEOGys4e4kqA+HpOW9XFDBInPWlKu1Nx0SP/gTC2h3bGKrcq6VwMxMT+Go75MPi+0Szqfx1xXJg8z57RG62XT1p2DSUqodJvGog5pt6ISIr9OZpyD91fEXFKizUkVmfZi9o4sTZZHs4+rAa/5yx7PEayf1GEzxEDGPFJl/aEFNCMw/YCU06DHlNg0UUmD2aFYwiXUuIUShd2GgV9AYRL5Co9bO/S25eQ61UmUo/LQt7x0YTWMgRxfen8qa6BS05SSsY/cZhM9Wy84CycoXeupks5eD9F7UhSsxqdCOpUTMPVXhVUQbDP8/NOa3+QUGh/jrDCDFkjrjETRsqzeinfdUxCE7F2v9c9MeFNb2rKupFqNzul+4wBVUOGNf5tl'
            }
        )

    async def parse(self, response):
        # print(response.text)
        resp_json = json.loads(response.text)
        for row in resp_json[0]:
            new_url = row['r'] + row['u'] + '.html'
            contact = row['contact']
            title = row['title']
            times = row['times']
            ennum = row['ennum']
            cardnum = row['cardnum']
            data = {'contact': contact, 'title': title, 'times': times, 'ennum': ennum, 'cardnum': cardnum, 'url': new_url}
            self.logger.info(data)
            yield ReSpider.Request(
                url=new_url,
                headers={
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Origin': 'http://data.showsfinder.com',
                    'Referer': 'http://data.showsfinder.com/pKz6qgBMyXjVL0v1MqAvpAblEeaPNOwR8.html',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cookie': self.cookies
                },
                priority=0,
                meta=data,
                callback=self.parse2
            )

    def parse2(self, response):
        meta = response.meta
        # self.logger.debug(meta)
        resp_text = response.text
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
    Testing4().start()
