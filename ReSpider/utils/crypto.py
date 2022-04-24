# -*- coding: utf-8 -*-
# @Time    : 2022/4/24 16:34
# @Author  : ZhaoXiangPeng
# @File    : crypto.py

import hashlib

__all__ = [
    "get_md5",
    "get_sha1",
    "get_sha224",
    "get_sha256",
    "get_sha384",
    "get_sha512"
]


def get_md5(arg) -> str:
    """
    生成md5
    :param arg:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(arg.encode(encoding='utf-8'))
    return md5.hexdigest()


# SHA
def get_sha1(arg) -> str:
    sha1 = hashlib.sha1()
    arg = arg.encode(encoding='utf-8')
    sha1.update(arg)
    return sha1.hexdigest()


def get_sha224(arg) -> str:
    return hashlib.sha224(
        arg.encode(encoding='utf-8')).hexdigest()


def get_sha256(arg) -> str:
    sha256 = hashlib.sha256()
    arg = arg.encode(encoding='utf-8')
    sha256.update(arg)
    return sha256.hexdigest()


def get_sha384(arg) -> str:
    return hashlib.sha384(
        arg.encode(encoding='utf-8')).hexdigest()


def get_sha512(arg) -> str:
    return hashlib.sha512(
        arg.encode(encoding='utf-8')).hexdigest()


if __name__ == '__main__':
    print(get_sha384("Nobody inspects the spammish repetition"))
