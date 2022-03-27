# -*- coding: utf-8 -*-
# @Time    : 2022/3/26 23:00
# @Author  : ZhaoXiangPeng
# @File    : make_class.py

import json
from ..http import Request, Response


def to_dict(other):
    return json.loads(other) if type(other) != dict else other


def make_req_from_json(other):
    obj: dict = to_dict(other)
    return Request.make_request(obj)


def make_res_from_json(other):
    obj: dict = to_dict(other)
    return Response(**obj)


def make_class(obj, init, **kwargs):
    try:
        init = to_dict(init)
    except json.JSONDecodeError:
        pass
    else:
        init.update(**kwargs)
    return obj(**init)
