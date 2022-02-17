# -*- coding: utf-8 -*-
# @Time    : 2022/2/17 8:37
# @Author  : ZhaoXiangPeng
# @File    : asyncio_test.py

import asyncio
import time


async def process(id_):
    print('当前id: ', id_)
    await asyncio.sleep(id_)


def process2(id_):
    print('当前id: ', id_)
    time.sleep(id_)


async def main():
    for i in range(1, 7):
        loop.create_task(process2(i))
    await asyncio.sleep(10)


if __name__ == '__main__':
    s = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(e)
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.stop()
    print(time.time() - s)

