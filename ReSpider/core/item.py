# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 18:00
# @Author  : ZhaoXiangPeng
# @File    : item.py

from typing import List

__all__ = [
    'Item',
    'DataItem',
    'DataListItem',
    'IoItem',
    'FileItem',
    'CSVItem',
    'CSVListItem',
    'RdsItem',
]


class ItemMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        # attrs['set_attribute'] = mcs.set_attribute
        return type.__new__(mcs, name, bases, attrs)

    def set_attribute(self, **kwargs):
        for key, val in kwargs.items():
            self.__dict__[key] = val


class Item(metaclass=ItemMetaclass):
    pass


class ArrayItem(List[dict]):
    def set_attribute(self, **kwargs):
        for key, val in kwargs.items():
            self.__dict__[key] = val


class DataItem(dict, Item):
    pipeline = 'MongoDBPipeline'
    collection = None

    def __init__(self, arg=None, **kwargs):
        if arg is None:
            arg = {}
        self.__dict__ = kwargs or self.__dict__
        super().__init__(self, **arg)

    def set_attribute(self, collection=None, **kwargs):
        self.collection = collection


class DataListItem(ArrayItem, Item):
    pipeline = 'MongoDBPipeline'
    collection = None

    def set_attribute(self, collection=None, **kwargs):
        self.collection = collection


class IoItem(bytes, Item):
    pipeline = 'FilePipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = None
    mode: str = 'w'

    def set_attribute(self,
                      data_directory=None,
                      filename=None,
                      filetype=None,
                      mode=None, **kwargs):
        self.data_directory = data_directory
        self.filename = filename
        self.filetype = filetype
        self.mode = mode or self.mode


class FileItem(str, Item):
    pipeline = 'FilePipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = None
    mode: str = 'w'
    encoding: str = 'utf-8'

    def set_attribute(self,
                      data_directory=None,
                      filename=None,
                      filetype=None,
                      mode=None,
                      encoding=None, **kwargs):
        self.data_directory = data_directory
        self.filename = filename
        self.filetype = filetype
        self.mode = mode or self.mode
        self.encoding = encoding or self.encoding


class CSVItem(dict, Item):
    pipeline = 'CSVPipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = 'csv'
    mode: str = 'a'
    encoding: str = 'utf-8'
    fieldnames = None

    def __init__(self, arg=None, **kwargs):
        if arg is None:
            arg = {}
        self.__dict__ = kwargs or self.__dict__
        super().__init__(self, **arg)


class CSVListItem(ArrayItem, Item):
    pipeline = 'CSVPipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = 'csv'
    mode: str = 'a'
    encoding: str = 'utf-8'
    fieldnames = None

    def set_attribute(self,
                      data_directory=None,
                      filename=None,
                      mode=None,
                      encoding=None,
                      fieldnames=None, **kwargs):
        self.data_directory = data_directory
        self.filename = filename
        self.mode = mode or self.mode
        self.encoding = encoding or self.encoding
        self.fieldnames = fieldnames or self[0].keys() if len(self) else []


class RdsItem(dict, Item):
    pipeline: str = 'RedisPipeline'
    rds_type: str = 'LIST'
    keys: str = None

    def __init__(self, arg=None, **kwargs):
        if arg is None:
            arg = {}
        self.__dict__ = kwargs or self.__dict__
        super().__init__(self, **arg)
