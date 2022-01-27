# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 9:48
# @Author  : ZhaoXiangPeng
# @File    : metaclass.py

from typing import List


class BytesMetaclass(type):
    def __new__(cls, name, bases, attrs, *args, **kwargs):
        attrs['data_directory'] = 'H:/'
        return type.__new__(cls, name, bases, attrs)


class MyBytes(bytes, metaclass=BytesMetaclass):
    data_directory=''
    pass


class ItemMetaclass(type):
    def __new__(mcs, *args, **kwargs):
        return type.__new__(mcs, *args, **kwargs)


class Item(metaclass=ItemMetaclass):
    pass


class DataItems(List[Item], metaclass=ItemMetaclass):
    pass


class FileItem(bytes or str, Item):
    pipeline = 'FilePipeline'
    def __init__(self, arg, **kwargs):
        super().__init__(arg)
        for k, v in kwargs:
            self[k] = v

    def __setattr__(self, key, value):
        self[key] = value
    pass

class TestItem:
    data_directory = 'a'
class BytesItem(bytes, TestItem):
    x = ''


f = FileItem(b'hello world', pipeline='a')
print(f)
f.m = 'b'

b = MyBytes(b'hello world')
b.a = 'c'
print(b)
print(b.data_directory)
