# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 22:52
# @Author  : ZhaoXiangPeng
# @File    : dupefilter.py

from ReSpider.dupefilter import DupeFilters
from ReSpider.db.redisdb import RedisDB
import ReSpider.setting as setting

__all__ = [
    "RFPDupeFilters"
]


class RFPDupeFilters(DupeFilters):
    def __init__(self, server=None, key=None, **kwargs):
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, server=None, **kwargs):
        if server is None:
            server = RedisDB()
        return cls(server=server, **kwargs)

    def verify_fingerprint(self, request) -> bool:
        """
        验证指纹是否存在, 存在 -> True; 不存在 -> 添加 -> False
        :return: 1 or 0
        """
        fp = request.fingerprint
        # 如果影响行数是0: 存在 -> True; 否则 -> False
        added = self.server.sadd(self.key, fp)  # 影响行数
        return added == 0


if __name__ == '__main__':
    RFPDupeFilters.from_settings()