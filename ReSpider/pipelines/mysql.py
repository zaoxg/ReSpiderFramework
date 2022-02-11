# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 15:37
# @Author  : ZhaoXiangPeng
# @File    : mysql.py

from . import BasePipeline
import re


class MySQLPipeline(BasePipeline):
    name = 'mysql pipeline'

    def sql_from_dict(self, ema_item, spider):
        """
        :param ema_item:  item ,  table_name_dict: setting中设置的 item名和表名对应字典
        :return:
        """
        try:
            item_name = re.findall('\.([A-Z]\w*)', str(type(ema_item)))  # 表名key
            table_name = self.table_name_dict[item_name[0]]  # 从配置的dict 对应的item 取出表名
            table_keys = list(ema_item.keys())
            sql = f'insert into {table_name} {tuple(table_keys)} values ({"%s," * (len(table_keys) - 1) + "%s"})'.replace(
                "'", "")
            vs = [ema_item[i] for i in table_keys]  # 根据key值列表生成值的元组
            vs_list = []
            for i in vs:
                i = '' if not i else i
                vs_list.append(i)
            vs = tuple(vs_list)
            return sql, vs
        except Exception as e:
            spider.logger.warning(f'sql_from_dict error: {e}')
