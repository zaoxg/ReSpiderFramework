# -*- coding: utf-8 -*-
# @Time    : 2022/4/20 16:49
# @Author  : ZhaoXiangPeng
# @File    : dupefilter.py

import os
import ReSpider.setting as setting

__all__ = [
    "DupeFilters",
    "RFPDupeFilters"
]


class DupeFilters:

    @classmethod
    def from_settings(cls, **kwargs):
        return cls()

    def open(self):
        pass

    def close(self):
        """
        后续添加debug模式, 结束后删除指纹库
        """
        pass

    def verify_fingerprint(self, request):
        return False


class RFPDupeFilters(DupeFilters):
    def __init__(self, path=None):
        self.file = None
        self.fingerprints = set()
        if path:
            self.file = open(os.path.join(path, 'requests.fps'), 'a+')
            self.file.seek(0)
            self.fingerprints.update(x.rstrip() for x in self.file)

    @classmethod
    def from_settings(cls, **kwargs):
        # 搞个磁盘缓存去重
        path = setting.WORKER_PATH
        return cls(path=path)

    def verify_fingerprint(self, request) -> bool:
        """
        验证指纹是否存在, 存在 -> True; 不存在 -> 添加 -> False
        """
        fp = request.fingerprint
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp+'\n')
        return False
