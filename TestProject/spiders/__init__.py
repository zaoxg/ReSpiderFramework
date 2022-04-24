# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 17:12
# @Author  : ZhaoXiangPeng
# @File    : __init__.py

# from ReSpider.utils.crypto import get_md5
import ReSpider
import sys
import os
sys.path.append(os.getcwd().replace('\\spiders', '').rsplit('\\', maxsplit=1)[0])
print(sys.path)
