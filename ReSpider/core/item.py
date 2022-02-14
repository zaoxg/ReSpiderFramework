# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 18:00
# @Author  : ZhaoXiangPeng
# @File    : item.py

from collections import UserList, UserString

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


class Item:
    """
    仅占用一个类型
    """
    pass


class MyArray(UserList):
    # 继承自 UserList, 修改 __init__ 以支持传参
    def __init__(self, initlist=None, **kwargs):
        super().__init__()
        self.data = []
        if initlist is not None:
            # XXX should this accept an arbitrary sequence?
            if type(initlist) == type(self.data):
                self.data[:] = initlist
            elif isinstance(initlist, UserList):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def set_attribute(self, **kwargs):
        for key, val in kwargs.items():
            self.__dict__[key] = val


class MyBytes:
    data: bytes = None

    def __init__(self, initbytes=None, **kwargs):
        if initbytes is not None:
            self.data = initbytes
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __float__(self): return float(self.data)
    def __hash__(self): return hash(self.data)
    def __len__(self): return len(self.data)

    def __eq__(self, string):
        if isinstance(string, MyBytes):
            return self.data == string.data
        return self.data == string

    def __contains__(self, char):
        if isinstance(char, MyBytes):
            char = char.data
        return char in self.data

    def __getitem__(self, index): return self.__class__(self.data[index])

    def __add__(self, other):
        if isinstance(other, MyBytes):
            return self.__class__(self.data + other.data)
        elif isinstance(other, bytes):
            return self.__class__(self.data + other)
        return self.__class__(self.data + bytes(other))

    def __radd__(self, other):
        if isinstance(other, bytes):
            return self.__class__(other + self.data)
        return self.__class__(bytes(other) + self.data)

    def __mul__(self, n): return self.__class__(self.data*n)
    __rmul__ = __mul__

    def hex(self, sep='', bytes_per_sep=1):
        if isinstance(self.data, bytes):
            return self.data.hex()

    def decode(self, encoding='utf-8', errors='strict'):
        encoding = 'utf-8' if encoding is None else encoding
        errors = 'strict' if errors is None else errors
        return self.data.decode(encoding, errors)

    def title(self):
        return self.__class__(self.data.title())


class MyStr(UserString):
    data: str = None

    def __init__(self, seq, **kwargs):
        super().__init__(seq)
        if isinstance(seq, str):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
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


class DataListItem(MyArray, Item):
    pipeline = 'MongoDBPipeline'
    collection = None

    def set_attribute(self, collection=None, **kwargs):
        self.collection = collection


class IoItem(MyBytes, Item):
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


class FileItem(MyStr, Item):
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


class CSVListItem(MyArray, Item):
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
