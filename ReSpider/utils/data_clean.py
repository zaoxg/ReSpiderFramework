# -*- coding: utf-8 -*-
# @Time    : 2021/10/8 16:15
# @Author  : ZhaoXiangPeng
# @File    : data_clean.py

import re


def a(string: str):
    string = "营口东.邦环保科技股份有限公司"

    a = re.split('[【|】|{|}|\[|\]|；|、|。|,|。|，|，|！|\!|\.|？| |～|\?\s]', string)
    return "".join(a)


def filter_emoji(desstr, restr=''):
    """
    过滤表情
    """
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF]')
    return co.sub(restr, desstr)
