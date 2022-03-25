# -*- coding: utf-8 -*-
# @Time    : 2022/1/6 10:24
# @Author  : ZhaoXiangPeng
# @File    : tools.py

import json
import re
import os
import time
import datetime
import base64


def get_current_timestamp():
    return int(time.time())


def get_current_date(date_format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(date_format)


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
    cookie_list = []
    for k, v in cookies.items():
        cookie_list.append(k+'='+v)
    return '; '.join(cookie_list)


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


def get_table_row_data(table, custom='string(.)', default=''):
    """
    获取表格里每一行数据
    @summary: Copy from https://github.com/Boris-code/feapder/blob/master/feapder/utils/tools.py  549
    @param table: 使用selector封装后的具有xpath的selector
    @param custom: 自定义xpath, 用于匹配列值
    @param default: 未匹配到时替换的值
    @return: [[],[]..]
    """
    datas = []
    rows = table.xpath(".//tr")
    for row in rows:
        cols = row.xpath("./td|./th")
        row_datas = []
        for col in cols:
            data = col.xpath(custom).extract_first(default).strip()
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
    if len(rows) < (1 if keys else 2):  # 先判断一下是不是空的, 如果为空直接返回, 防止后面通过索引取值时报错 IndexError
        return datas
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


def hump2underline(source_str: str):
    """
    驼峰形式字符串转成下划线形式
        mediaType -> media_type
    :param source_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    """
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', source_str).lower()
    return sub


def underline2hump(source_str: str):
    """
    下划线形式字符串转成驼峰形式
    :param source_str: 下划线形式字符串
    :return: 驼峰形式字符串
    """
    sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), source_str)
    return sub


def firstCharUpper(source_str: str):
    # 首字母大写转换函数
    return source_str[:1].upper() + source_str[1:]


################################
def extract_dict(source_dict: dict, keys=None) -> dict:
    """
    # @summary: 从一个字典中提取字典
    :param source_dict: 需要提取key的原字典
    :param keys: 提取的key, <iterable>
    :return:
    """
    if keys is None:
        raise ValueError('if <key> is None, I suggest you use %s' % source_dict)
    return {key: val for key, val in source_dict.items() if key in keys}

################################
def mkdir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as exc:  # Python >2.5
        pass


def is_exist(file_path):
    """
    @summary: 文件是否存在
    ---------
    @param file_path:
    ---------
    @result:
    """

    return os.path.exists(file_path)


def read_file(filename, readlines=False, encoding="utf-8"):
    """
    @summary: 读文件
    ---------
    @param filename: 文件名（有路径）
    @param readlines: 按行读取 （默认False）
    ---------
    @result: 按行读取返回List，否则返回字符串
    """

    content = None
    try:
        with open(filename, "r", encoding=encoding) as file:
            content = file.readlines() if readlines else file.read()
    except Exception as e:
        raise e

    return content


def str2base64(s: str = None):
    if s is None:
        raise ValueError("ckbnm")
    encoder = base64.b64encode(s.encode("utf-8"))
    str_encoder = encoder.decode('utf-8')
    return str_encoder


def base64_to_str(s: str = None):
    if s is None:
        raise ValueError("ckjnm")
    decoder = base64.b64decode(s)
    return decoder

'''
def exec_js(js_code):
    """
    @summary: 执行js代码
    @param js_code: js代码
    @result: 返回执行结果
    """
    return execjs.eval(js_code)


def compile_js(js_func):
    """
    @summary: 编译js函数
    @param js_func:js函数
    @result: 返回函数对象 调用 fun('js_funName', param1,param2)
    """

    ctx = execjs.compile(js_func)
    return ctx.call
'''
