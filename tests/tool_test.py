# -*- coding: utf-8 -*-
# @Time    : 2022/3/28 10:00
# @Author  : ZhaoXiangPeng
# @File    : tool_test.py

import ReSpider.utils.tools as tools

print(tools.make_sql_from_('website', {'name': 'runoob', 'url': 'www.runoob.com'}))
