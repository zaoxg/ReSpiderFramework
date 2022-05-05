# -*- coding: utf-8 -*-
# @Time    : 2022/4/24 16:57
# @Author  : ZhaoXiangPeng
# @File    : pyjs.py

import time


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


def getTime():
    return int(time.time()*1000)


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