# -*- coding: utf-8 -*-
# @Time    : 2022/4/18 16:44
# @Author  : ZhaoXiangPeng
# @File    : token_bucket.py

import time


class TokenBucket:

    # rate是令牌发放速度，capacity是桶的大小
    def __init__(self, rate, capacity):
        self._rate = rate
        self._capacity = capacity
        self._current_amount = 0
        self._last_consume_time = int(time.time())

    # token_amount是发送数据需要的令牌数
    def consume(self, token_amount=1):
        increment = (int(time.time()) - self._last_consume_time) * self._rate  # 计算从上次发送到这次发送，新发放的令牌数量
        self._current_amount = min(
            increment + self._current_amount, self._capacity)  # 令牌数量不能超过桶的容量
        if token_amount > self._current_amount:  # 如果没有足够的令牌，则不能发送数据
            return False
        self._last_consume_time = int(time.time())
        self._current_amount -= token_amount
        return True


if __name__ == '__main__':
    tb = TokenBucket(5, 10)
    s = time.time()
    print(s)
    while 1:
        if tb.consume(1):
            print('hello world')
            print(time.time())
        else:
            print('cache')
