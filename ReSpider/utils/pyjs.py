# -*- coding: utf-8 -*-
# @Time    : 2022/4/24 16:57
# @Author  : ZhaoXiangPeng
# @File    : pyjs.py

import time
import ctypes


def charCodeAt(s: str, i: int = 0):
    # 'A'.charCodeAt(0) -> 65
    return ord(s[i])


def charAt(s: str, index: int = 0):
    if index < len(s):
        return s[index]
    return ''


def fromCharCode(n: int):
    return chr(n)


def slice_(s: list or str, start, end: int = None):
    if end is None:
        return s[start:]
    return s[start: end]


# ################################################# 数组操作 ################################################# #
def shift(arr: list):
    """
    方法从数组中删除第一个元素，并返回该元素的值。此方法更改数组的长度
    从数组中删除的元素; 如果数组为空则返回 undefined(None)
    """
    if len(arr):
        return arr.pop(0)
    return None


def unshift(arr: list, *args):
    """
    将一个或多个元素添加到目录中，并返回该方法的新长度（该方法原有修改目录）
    """
    arr[0:0] = args
    return len(arr)


def getTime():
    return int(time.time() * 1000)


def parseInt(i, j: int = None):
    if j is None:
        j = 10
    return int(i, j)


def number_join(array: list, seq: str):
    bool_map = {'True': 'true', 'False': 'false', 'None': 'undefined'}
    new_array = []
    for a in array:
        if not isinstance(a, str):
            if str(a) in bool_map:
                a = bool_map[str(a)]
        new_array.append(str(a))
    return seq.join(new_array)


def int_overflow(val):
    # 这个函数可以得到32位int溢出结果，因为python的int一旦超过宽度就会自动转为long，永远不会溢出，有的结果却需要溢出的int作为参数继续参与运算
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shift(n, i):
    # 无符号右移
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    # print(n)
    return int_overflow(n >> i)


def left_shift(x, y):
    return ctypes.c_int(x << y).value
