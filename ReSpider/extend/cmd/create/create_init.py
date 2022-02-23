# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 17:25
# @Author  : ZhaoXiangPeng
# @File    : create_init.py

import json


class CreateInit:
    def create(self):
        __all__ = []

        import os

        path = os.getcwd()
        for file in os.listdir(path):
            if file.endswith(".py") and not file.startswith("__init__"):
                model = file.split(".")[0]
                __all__.append(model)

        del os

        with open("__init__.py", "w", encoding="utf-8") as file:
            text = "__all__ = %s" % json.dumps(__all__, ensure_ascii=False)
            file.write(text)
