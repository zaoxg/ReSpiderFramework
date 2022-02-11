# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 18:00
# @Author  : ZhaoXiangPeng
# @File    : item.py

from typing import List


class ItemMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        attrs['set_attribute'] = mcs.set_attribute
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

    def set_attribute(self, collection, **kwargs):
        self.collection = collection


class DataListItem(ArrayItem, Item):
    pipeline = 'MongoDBPipeline'
    collection = None

    def set_attribute(self, collection, **kwargs):
        self.collection = collection


class IoItem(bytes, Item):
    pipeline = 'FilePipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = None
    mode: str = 'w'

    def set_attribute(self, data_directory, filename, filetype, mode, **kwargs):
        self.data_directory = data_directory
        self.filename = filename
        self.filetype = filetype
        self.mode = mode


class FileItem(str, Item):
    pipeline = 'FilePipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = None
    mode: str = 'w'
    encoding: str = 'utf-8'

    def set_attribute(self, data_directory, filename, filetype, mode, encoding, **kwargs):
        self.data_directory = data_directory
        self.filename = filename
        self.filetype = filetype
        self.mode = mode
        self.encoding = encoding


class CSVItem(dict, Item):
    pipeline = 'CSVPipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = 'csv'
    mode: str = 'a'
    encoding: str = 'utf-8'

    def set_attribute(self, data_directory, filename, filetype, mode, encoding, **kwargs):
        self.data_directory = data_directory
        self.filename = filename
        self.filetype = filetype
        self.mode = mode
        self.encoding = encoding


class CSVListItem(ArrayItem, Item):
    pipeline = 'CSVPipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = 'csv'
    mode: str = 'a'
    encoding: str = 'utf-8'

    def set_attribute(self, data_directory, filename, filetype, mode, encoding, **kwargs):
        self.data_directory = data_directory
        self.filename = filename
        self.filetype = filetype
        self.mode = mode
        self.encoding = encoding


class RdsItem(dict, Item):
    pipeline: str = 'RedisPipeline'
    rds_type: str = 'LIST'
    keys: str = None

    def set_attribute(self, rds_type, keys, **kwargs):
        self.rds_type = rds_type
        self.keys = keys
