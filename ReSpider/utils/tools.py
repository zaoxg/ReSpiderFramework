# -*- coding: utf-8 -*-
# @Time    : 2022/1/6 10:24
# @Author  : ZhaoXiangPeng
# @File    : tools.py
import json
import re


def get_cookies_from_str(cookie_str: str):
    """
    @summary: 自己懒得写, Copy from https://github.com/Boris-code/feapder/blob/master/feapder/utils/tools.py
    >>> get_cookies_from_str("key=value; key2=value2; key3=; key4=; ")
    {'key': 'value', 'key2': 'value2', 'key3': '', 'key4': ''}
    Args:
        cookie_str: key=value; key2=value2; key3=; key4=
    Returns:
    """
    cookies = {}
    for cookie in cookie_str.split(";"):
        cookie = cookie.strip()
        if not cookie:
            continue
        key, value = cookie.split("=", 1)
        key = key.strip()
        value = value.strip()
        cookies[key] = value

    return cookies


def cookiejar2str(cookies: dict):
    """
    cookie字典转字符串
    """
    cookie_str = ''
    for k, v in cookies.items():
        cookie_str += k
        cookie_str += '='
        cookie_str += v
        cookie_str += '; '
    return cookie_str


def table_json(table, save_one_blank=True):
    """
    将表格转为json 适应于 key：value 在一行类的表格
    @summary: Copy from https://github.com/Boris-code/feapder/blob/master/feapder/utils/tools.py  521
    @param table: 使用selector封装后的具有xpath的selector
    @param save_one_blank: 保留一个空白符
    @return:
    """
    data = {}

    trs = table.xpath(".//tr")
    for tr in trs:
        tds = tr.xpath("./td|./th")

        for i in range(0, len(tds), 2):
            if i + 1 > len(tds) - 1:
                break

            key = tds[i].xpath("string(.)").extract_first(default="").strip()
            value = tds[i + 1].xpath("string(.)").extract_first(default="").strip()
            value = replace_str(value, "[\f\n\r\t\v]", "")
            value = replace_str(value, " +", " " if save_one_blank else "")

            if key:
                data[key] = value

    return data


def get_table_row_data(table):
    """
    获取表格里每一行数据
    @summary: Copy from https://github.com/Boris-code/feapder/blob/master/feapder/utils/tools.py  549
    @param table: 使用selector封装后的具有xpath的selector
    @return: [[],[]..]
    """

    datas = []
    rows = table.xpath(".//tr")
    for row in rows:
        cols = row.xpath("./td|./th")
        row_datas = []
        for col in cols:
            data = col.xpath("string(.)").extract_first(default="").strip()
            row_datas.append(data)
        datas.append(row_datas)

    return datas


def rows2json(rows, keys=None):
    """
    将行数据转为json
    @summary: Copy from https://github.com/Boris-code/feapder/blob/master/feapder/utils/tools.py  569
    @param rows: 每一行的数据
    @param keys: json的key，空时将rows的第一行作为key
    @return:
    """
    data_start_pos = 0 if keys else 1
    datas = []
    keys = keys or rows[0]
    for values in rows[data_start_pos:]:
        datas.append(dict(zip(keys, values)))

    return datas


def jsonp2json(jsonp):
    """
    将jsonp转为json
    @summary: Copy from https://github.com/Boris-code/feapder/blob/master/feapder/utils/tools.py  815
    @param jsonp: jQuery172013600082560040794_1553230569815({})
    @return:
    """
    try:
        return json.loads(re.match(".*?({.*}).*", jsonp, re.S).group(1))
    except:
        raise ValueError("Invalid Input")


def replace_str(source_str, regex, replace_str=""):
    """
    916
    @summary: 替换字符串
    ---------
    @param source_str: 原字符串
    @param regex: 正则
    @param replace_str: 用什么来替换 默认为''
    ---------
    @result: 返回替换后的字符串
    """
    str_info = re.compile(regex)
    return str_info.sub(replace_str, source_str)
