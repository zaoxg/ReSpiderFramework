# -*- coding: utf-8 -*-
# @Time    : 2022/1/5 17:03
# @Author  : ZhaoXiangPeng
# @File    : cmd_arg_test1.py

import argparse

# 先创建一个 ArgumentParser 对象
# 对象包含将命令行解析成 Python 数据类型所需的全部信息
parser = argparse.ArgumentParser(description='Parser Test.')
parser.add_argument('-C', dest='CONCURRENT_REQUESTS', help='Concurrent Total.')
parser.add_argument('-D', dest='DOWNLOAD_DELAY', help='Download Delay.')

args = parser.parse_args()
print(args)
print(args.CONCURRENT_REQUESTS)
print(args.DOWNLOAD_DELAY)

