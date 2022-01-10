# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 11:08
# @Author  : ZhaoXiangPeng
# @File    : urlProcess.py

import json
from pprint import pprint
from urllib.parse import urlencode, urlparse, quote, unquote, parse_qs


def urlParse(url: str):
    """
    url解析为dict
    :param url:
    :return:
    """
    query = urlparse(url).query
    params = parse_qs(query)
    result = {key: params[key][0] if params[key].__len__() == 1 else params[key] for key in params}
    return result


def queryParse(query: str):
    string = unquote(query)
    params = string.split('&')
    formData = {}
    for param in params:
        kvs = param.split('=', maxsplit=1)
        k = kvs[0]
        v = kvs[-1]
        formData[k] = int(v) if v.isdigit() else v
    jsonFM = json.dumps(formData, ensure_ascii=False)
    return formData


def unquote_url(url: str, encoding='utf-8'):
    """
    @summary: url解码
    """
    return unquote(url, encoding=encoding)


def quote_url(url: str, safe='%;/?:@&=+$,', encoding='utf-8'):
    """
    @summary: url编码
    """
    return quote(url, safe=safe, encoding=encoding)


if __name__ == '__main__':
    # str1 = 'c_data=0&c_count=0&ischeckall=false&ischecknow=&pageindex=2&Groupname=&Groupvalue=&isSession=0&datafrom=&re_allsubject=0&re_booktype=1&re_startyear=1949&re_endyear=2018&re_Province=all&re_key=&re_keyv1=&re_keyv2=&re_unk=&re_un=&re_islike=&allsubject=0&booktype=1&startyear=2021&endyear=2021&f_startyear=1949&f_endyear=2021&Province=all&ishcited=0&isbcb=0&SearchType=4&key1=%E7%A7%91%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE&sislike=%3D&resultSearch=0&key=4%2C2%2C&keyv1=%E7%A7%91%E5%AD%A6%E5%87%BA%E7%89%88%E7%A4%BE%2C%2C&unk=&un=and%2C&islike=%3D%2C%3D%2C&num=100&WebPagerPageIndex=2&pagesize=50&allcheck=&checknow=&orderfunction=desc&orderfield=TotalCitedFrequency&IndexPage=3&PageSize=50'
    str1 = 'uqf=LS00009021&orderf=ImpactFactor&isSession=0&orderfun=desc&jisload=0&disload=0&cisload=0'
    FD = queryParse(str1)
    print(FD)
