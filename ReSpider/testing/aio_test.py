# -*- coding: utf-8 -*-
# @Time    : 2021/1/24 15:42
# @Author  : ZhaoXiangPeng
# @File    : aio_test.py


import asyncio
import time
import json

import aiohttp

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'https://kns.cnki.net/KNS8/AdvSearch?dbcode=CDMD',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://kns.cnki.net',
    'Connection': 'keep-alive',
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Referer': 'https://kns.cnki.net/kns8/AdvSearch?dbprefix=SCDB&&crossDbcodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCVD%2CCJFN%2CCCJD'
}


async def request(augment):
    timeout = aiohttp.ClientTimeout(total=15)
    conn = aiohttp.TCPConnector(ssl=False)
    response = None
    excepts = None
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            async with session.request(
                    method='POST',
                    url='https://kns.cnki.net/KNS8/Brief/GetGridTableHtml',
                    timeout=timeout,
                    headers=HEADER,
                    data=augment
            ) as response:
                print(response.headers)
                response = await response.text()

        except asyncio.exceptions.TimeoutError as timeOutError:
            # self.logger.error("请求超时异常", timeOutError, exc_info=True)
            excepts = timeOutError
        except aiohttp.ClientConnectorError as client_conn_error:
            # self.logger.error("客户端链接错误", client_conn_error, exc_info=True)
            excepts = client_conn_error
        except aiohttp.InvalidURL as invalid_url:
            # self.logger.error(invalid_url, exc_info=True)
            excepts = invalid_url
        except Exception as exception:
            # self.logger.error(exception)
            excepts = exception
        finally:
            await session.close()
            return dict(
                response=response,
                meta=augment,
                excepts=excepts
            )


arg = "IsSearch=true&QueryJson=%7B%22Platform%22%3A%22%22%2C%22DBCode%22%3A%22CJFQ%22%2C%22KuaKuCode%22%3A%22%22%2C%22QNode%22%3A%7B%22QGroup%22%3A%5B%7B%22Key%22%3A%22Subject%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A4%2C%22Items%22%3A%5B%7B%22Key%22%3A%22Expert%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A0%2C%22Name%22%3A%22%22%2C%22Operate%22%3A%22%22%2C%22Value%22%3A%22AF%25'%E5%86%9B'+OR+AF%25'%E9%83%A8%E9%98%9F'+OR+AF%25'%E6%AD%A6%E8%AD%A6'+OR+AF%25'%E6%80%BB'+OR+AF%25'%E5%A3%AB%E5%AE%98'+OR+AF%25'%E7%82%AE%E5%85%B5'+OR+AF%25'%E5%90%8E%E5%8B%A4'+OR+AF%25'%E4%BA%8C%E7%82%AE'%22%2C%22ExtendType%22%3A12%2C%22ExtendValue%22%3A%22%E4%B8%AD%E8%8B%B1%E6%96%87%E5%AF%B9%E7%85%A7%22%2C%22Value2%22%3A%22%22%2C%22BlurType%22%3A%22%22%7D%5D%2C%22ChildItems%22%3A%5B%5D%7D%2C%7B%22Key%22%3A%22ControlGroup%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A1%2C%22Items%22%3A%5B%5D%2C%22ChildItems%22%3A%5B%5D%7D%2C%7B%22Key%22%3A%22MutiGroup%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A1%2C%22Items%22%3A%5B%5D%2C%22ChildItems%22%3A%5B%7B%22Key%22%3A%223%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A1%2C%22Items%22%3A%5B%7B%22Key%22%3A%222012%22%2C%22Title%22%3A%222012%22%2C%22Logic%22%3A2%2C%22Name%22%3A%22%E5%B9%B4%22%2C%22Operate%22%3A%22%22%2C%22Value%22%3A%222012%22%2C%22ExtendType%22%3A0%2C%22ExtendValue%22%3A%22%22%2C%22Value2%22%3A%22%22%2C%22BlurType%22%3A%22%22%7D%5D%2C%22ChildItems%22%3A%5B%5D%7D%2C%7B%22Key%22%3A%226%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A1%2C%22Items%22%3A%5B%7B%22Key%22%3A%22E076%3F%22%2C%22Title%22%3A%22%E7%89%B9%E7%A7%8D%E5%8C%BB%E5%AD%A6%22%2C%22Logic%22%3A2%2C%22Name%22%3A%22%E4%B8%93%E9%A2%98%E5%AD%90%E6%A0%8F%E7%9B%AE%E4%BB%A3%E7%A0%81%22%2C%22Operate%22%3A%22%22%2C%22Value%22%3A%22E076%3F%22%2C%22ExtendType%22%3A14%2C%22ExtendValue%22%3A%22%22%2C%22Value2%22%3A%22%22%2C%22BlurType%22%3A%22%22%7D%5D%2C%22ChildItems%22%3A%5B%5D%7D%5D%7D%5D%7D%7D&PageName=DefaultResult&HandlerId=0&DBCode=CJFQ&KuaKuCodes=&CurPage=1&RecordsCntPerPage=20&CurDisplayMode=listmode&CurrSortField=%25e5%258f%2591%25e8%25a1%25a8%25e6%2597%25b6%25e9%2597%25b4%252f(%25e5%258f%2591%25e8%25a1%25a8%25e6%2597%25b6%25e9%2597%25b4%252c%2527TIME%2527)&CurrSortFieldType=desc&IsSortSearch=false&IsSentenceSearch=false&Subject="
arg1 = {'IsSearch': True, 'QueryJson': '{"Platform": "", "DBCode": "CJFQ", "KuaKuCode": "", "QNode": {"QGroup": [{"Key": "Subject", "Title": "", "Logic": 4, "Items": [{"Key": "Expert", "Title": "", "Logic": 0, "Name": "", "Operate": "", "Value": "AF%\'军\' OR AF%\'部队\' OR AF%\'武警\' OR AF%\'总\' OR AF%\'士官\' OR AF%\'炮兵\' OR AF%\'后勤\' OR AF%\'二炮\'", "ExtendType": 12, "ExtendValue": "中英文对照", "Value2": "", "BlurType": ""}], "ChildItems": []}, {"Key": "ControlGroup", "Title": "", "Logic": 1, "Items": [], "ChildItems": []}, {"Key": "MutiGroup", "Title": "", "Logic": 1, "Items": [], "ChildItems": [{"Key": "3", "Title": "", "Logic": 1, "Items": [{"Key": "2020", "Title": "2020", "Logic": 2, "Name": "年", "Operate": "", "Value": "2020", "ExtendType": 0, "ExtendValue": "", "Value2": "", "BlurType": ""}], "ChildItems": []}, {"Key": "6", "Title": "", "Logic": 1, "Items": [{"Key": "E072?", "Title": "肿瘤学", "Logic": 2, "Name": "专题子栏目代码", "Operate": "", "Value": "E072?", "ExtendType": 14, "ExtendValue": "", "Value2": "", "BlurType": ""}], "ChildItems": []}]}]}}', 'PageName': 'DefaultResult', 'HandlerId': 4, 'DBCode': 'CJFQ', 'KuaKuCodes': '', 'CurPage': 1, 'RecordsCntPerPage': 50, 'CurDisplayMode': 'listmode', 'CurrSortField': '%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27)', 'CurrSortFieldType': 'desc', 'IsSortSearch': False, 'IsSentenceSearch': False, 'Subject': ''}


print(asyncio.run(request(arg1)))
