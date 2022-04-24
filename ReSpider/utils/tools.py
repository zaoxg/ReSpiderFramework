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
import pickle
import functools
from urllib.parse import urlparse, quote, unquote, parse_qs


def get_current_timestamp():
    return int(time.time())


def get_current_date(date_format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(date_format)


def get_cookies_from_str(cookie_str: str):
    """
    @summary: 自己懒得写, Copy from https://github.com/Boris-code/feapder/blob/master/feapder/utils/tools.py
    >>> get_cookies_from_str("key=value; key2=value2; key3=; key4=; ")
    {'key': 'value', 'key2': 'value2', 'key3': '', 'key4': ''}
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


def url_parse(url: str):
    """
    url解析为dict
    :param url:
    :return:
    """
    query = urlparse(url).query
    params = parse_qs(query)
    result = {key: params[key][0] if params[key].__len__() == 1 else params[key] for key in params}
    return result


def query_parse(query: str):
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


def dumps_obj(obj):
    return pickle.dumps(obj)


def loads_obj(obj_s):
    return pickle.loads(obj_s)


def dumps_json(value, **kwargs):
    return json.dumps(value,
                      ensure_ascii=False, default=str, **kwargs)


def get_method(obj, func_name):
    try:
        return getattr(obj, func_name)
    except AttributeError:
        return None


def is_callable(obj):
    return (
        True
        if callable(obj)
        else False
    )


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


def del_special(string: str):
    """
    # :param string:
    # :return:
    """
    res = re.split('[【|】|{|}|\[|\]|；|、|。|,|。|，|，|！|\!|\.|？| |～|\?\s]', string)
    return "".join(res)


def filter_emoji(desstr, restr=''):
    """
    过滤表情
    """
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF]')
    return co.sub(restr, desstr)


def list2str(datas):
    """
    列表转字符串
    :param datas: [1, 2]
    :return: (1, 2)
    """
    data_str = str(tuple(datas))
    data_str = re.sub(",\)$", ")", data_str)
    return data_str


def format_sql_value(value):
    if isinstance(value, str):
        value = value.strip()

    elif isinstance(value, (list, dict)):
        value = dumps_json(value)

    elif isinstance(value, (datetime.date, datetime.time)):
        value = str(value)

    elif isinstance(value, bool):
        value = int(value)

    return value


def make_sql_insert(table, data):
    ls = [(k, v) for k, v in data.items() if v is not None]
    keys = ', '.join([i[0] for i in ls])
    values = ', '.join(repr(i[1]) for i in ls)
    sentence = f'INSERT INTO {table} ({keys}) VALUES ({values});'
    return sentence


def make_sql_update(table, data, condition):
    sentence = 'UPDATE {table} SET {key_values} WHERE {condition}'
    key_values = []
    for key, value in data.items():
        value = format_sql_value(value)
        if isinstance(value, str):
            key_values.append(f'{key}={repr(value)}')
        elif value is None:
            key_values.append(f'{key}=null')
        else:
            key_values.append(f'{key}={value}')
    key_values = ', '.join(key_values)
    condition = ' AND '.join([f'%s=%r' % (k, v) for k, v in condition.items()])
    sentence.format(table=table, key_values=key_values, condition=condition)
    return sentence


def make_batch_sql(
    table, datas, auto_update=False, update_columns=(), update_columns_value=()
):
    """
    @summary: 生产批量的sql
    ---------
    @param table:
    @param datas: 表数据 [{...}]
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    @param update_columns_value: 需要更新的列的值 默认为datas里边对应的值, 注意 如果值为字符串类型 需要主动加单引号， 如 update_columns_value=("'test'",)
    ---------
    @result:
    """
    if not datas:
        return

    keys = list(datas[0].keys())
    values_placeholder = ["%s"] * len(keys)

    values = []
    for data in datas:
        value = []
        for key in keys:
            current_data = data.get(key)
            current_data = format_sql_value(current_data)

            value.append(current_data)

        values.append(value)

    keys = ["`{}`".format(key) for key in keys]
    keys = list2str(keys).replace("'", "")

    values_placeholder = list2str(values_placeholder).replace("'", "")

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        if update_columns_value:
            update_columns_ = ", ".join(
                [
                    "`{key}`={value}".format(key=key, value=value)
                    for key, value in zip(update_columns, update_columns_value)
                ]
            )
        else:
            update_columns_ = ", ".join(
                ["`{key}`=values(`{key}`)".format(key=key) for key in update_columns]
            )
        sql = "insert into `{table}` {keys} values {values_placeholder} on duplicate key update {update_columns}".format(
            table=table,
            keys=keys,
            values_placeholder=values_placeholder,
            update_columns=update_columns_,
        )
    elif auto_update:
        sql = "replace into `{table}` {keys} values {values_placeholder}".format(
            table=table, keys=keys, values_placeholder=values_placeholder
        )
    else:
        sql = "insert ignore into `{table}` {keys} values {values_placeholder}".format(
            table=table, keys=keys, values_placeholder=values_placeholder
        )

    return sql, values


def retry(retry_times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
        return wrapper
    return decorator


def exception_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].logger.warning(e, exec_info=True)
    return wrapper


def spilt_path(path: str) -> tuple:
    """
    :param path: 输入一个文件的全路径，将文件名和路径分割开
    如果给出的是一个目录和文件名，则输出路径和文件名
    如果给出的是一个目录名，则输出路径和为空文件名
    仅仅是以 "PATH" 中最后一个 '/' 作为分隔符，分隔后，将索引为0的视为目录（路径），将索引为1的视为文件名
    """
    return os.path.split(path)


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
