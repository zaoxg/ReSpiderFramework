# -*- coding: utf-8 -*-
# @Time    : 2022/4/22 16:52
# @Author  : ZhaoXiangPeng
# @File    : __init__.py.py

class ReQueue:
    """
    TODO
    基础的任务队列类, 实现put和get
    目的: 子类实现响应的接口, 在调度其中同意调用接口而不是在调度器中实现, 尽量让调度器代码简介, 并可以复用
    """
    def put(self, item, **kwargs):
        pass

    def get(self, **kwargs):
        pass
