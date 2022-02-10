# -*- coding: utf-8 -*-
# @Time    : 2022/1/7 16:32
# @Author  : ZhaoXiangPeng
# @File    : 2.py

import asyncio
import time

import aiohttp


async def fetch(session, id_, url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        async with session.get(url, headers=headers, verify_ssl=False) as resp:
            print(time.time(), resp.status)
            return await resp.text(), await resp.read()
    except Exception:
        print(f"{id_}, url: {url} error happened:")


async def fetch_all(urls):
    '''
    urls: list[(id_, url)]
    '''
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False, limit=1)
    ) as session:
        datas = await asyncio.gather(*[fetch(session, id_, url) for id_, url in urls], return_exceptions=True)
        # return_exceptions=True 可知从哪个url抛出的异常
        for ind, data in enumerate(urls):
            id_, url = data
            if isinstance(datas[ind], Exception):
                print(f"{id_}, {url}: ERROR")
        return datas


s = time.time()
urls = [(i, 'http://127.0.0.1:8000/') for i in range(500)]
loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_all(urls))
loop.close()
print(time.time() - s)
