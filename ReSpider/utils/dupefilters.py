# -*- coding: utf-8 -*-
# @Time    : 2021/1/24 21:22
# @Author  : ZhaoXiangPeng
# @File    : dupefilters.py
"""
请求指纹fingerprint
使用md5
"""
import hashlib


def encrypt_md5(arg):
    """
    生成md5
    :param arg:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(arg.encode(encoding='utf-8'))
    return md5.hexdigest()
