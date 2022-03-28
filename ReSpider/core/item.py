# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 18:00
# @Author  : ZhaoXiangPeng
# @File    : item.py

__all__ = [
    'Item',
    'DataItem',
    'DataListItem',
    'IoItem',
    'FileItem',
    'CSVItem',
    'CSVListItem',
    'RdsItem',
    'RdsItemHash',
    'RdsListItem'
]

from collections import UserList, UserString, UserDict
import json


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
    data = None

    def __len__(self): return len(self.data)

    def __contains__(self, item): return item in self.data

    def __setitem__(self, i, item): self.data[i] = item

    def __str__(self): return self.data

    def __repr__(self): return repr(self.data)

    def __iter__(self):
        for obj in self.data if type(self.data) is dict else self.data.items():
            yield obj


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


class MyBytes:
    data: bytes = None

    def __init__(self, initbytes=None, **kwargs):
        if initbytes is not None:
            self.data = initbytes
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

    def __int__(self):
        return int(self.data)

    def __float__(self):
        return float(self.data)

    def __hash__(self):
        return hash(self.data)

    def __len__(self):
        return len(self.data)

    def __eq__(self, string):
        if isinstance(string, MyBytes):
            return self.data == string.data
        return self.data == string

    def __contains__(self, char):
        if isinstance(char, MyBytes):
            char = char.data
        return char in self.data

    def __getitem__(self, index):
        return self.__class__(self.data[index])

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

    def __mul__(self, n):
        return self.__class__(self.data * n)

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

    def __init__(self, initdict=None, collection=None, **kwargs):
        if initdict is None:
            initdict = {}
        super().__init__(self, **initdict)
        self.collection = collection
        for key, val in kwargs.items():
            self.__dict__[key] = val


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
    mode: str = 'wb'  # bytes 写入 wb
    encoding: str = None

    def set_attribute(self,
                      data_directory=None,
                      filename=None,
                      filetype=None,
                      mode=None, **kwargs):
        self.data_directory = data_directory
        self.filename = str(filename)
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
        self.filename = str(filename)
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
    __fieldnames = None

    def __init__(self, initdict=None,
                 data_directory=None, filename=None,
                 mode=None, encoding=None, fieldnames=None,
                 **kwargs):
        if initdict is None:
            initdict = {}
        super().__init__(self, **initdict)
        self.data_directory = data_directory
        self.filename = str(filename)
        if mode:
            self.mode = mode
        if encoding:
            self.encoding = encoding
        self.fieldnames = fieldnames or self.keys()
        for key, val in kwargs.items():
            self.__dict__[key] = val

    @property
    def fieldnames(self):
        if self.__fieldnames is None:
            self.__fieldnames = self[0].keys() if len(self) else []
        return self.__fieldnames

    @fieldnames.setter
    def fieldnames(self, val):
        if self.__fieldnames != val:
            self.__fieldnames = val


class CSVListItem(MyArray, Item):
    pipeline = 'CSVPipeline'
    data_directory: str = None
    filename: str = None
    filetype: str = 'csv'
    mode: str = 'a'
    encoding: str = 'utf-8'
    __fieldnames = None

    def __init__(self,
                 initlist=None, data_directory=None, filename=None,
                 mode=None, encoding=None, fieldnames=None,
                 **kwargs):
        super().__init__(initlist=initlist, **kwargs)
        self.data_directory = data_directory
        self.filename = str(filename)
        if mode:
            self.mode = mode
        if encoding:
            self.encoding = encoding
        self.__fieldnames = fieldnames or (self[0].keys() if len(self) else None)

    @property
    def fieldnames(self):
        if self.__fieldnames is None:
            self.__fieldnames = self[0].keys() if len(self) else []
        return self.__fieldnames

    @fieldnames.setter
    def fieldnames(self, val):
        if self.__fieldnames != val:
            self.__fieldnames = val

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


class RdsItem(Item):
    pipeline: str = 'RedisPipeline'
    rds_type: str = 'LIST'
    key: str = None
    __auto_serialize: False

    def __init__(self, initval=None,
                 key: str = None, rds_type: str = None,
                 auto_serialize: bool = True, **kwargs):
        self.key = key
        self.rds_type = rds_type or self.rds_type
        self.__auto_serialize = auto_serialize
        if initval is not None:
            container = {'LIST': [], 'SET': [], 'HASH': {}}
            self.data = container[self.rds_type]
        # if type(initval) == type(self.data):
        if isinstance(initval, type(self.data)):
            self.data = initval
        elif type(self.data) == list:
            self.append(initval)
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def __iter__(self):
        for obj in self.data:
            yield obj

    def append(self, item, serialize=False) -> None:
        """
        :param item: 数据实体
        :param serialize: if to_json is True -> JSON(item)
        :return:
        """
        # 只有<list>才有append方法, 所以需要先转换为list
        if self.__auto_serialize:
            item = json.dumps(item, ensure_ascii=False)
        self.data.append(item)


class RdsItemHash(RdsItem):
    rds_type = 'HASH'

    def __delitem__(self, key): del self.data[key]

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        raise KeyError(key)

    def __iter__(self):
        for obj in self.data.items():
            yield obj

    def items(self):
        return self.data.items()

    def update(self, item):
        if item is not None:
            self.data.update(item)

    def append(self, item, serialize=False):
        raise AttributeError("'%s' object has no attribute 'append'" % self.data.__class__.__name__)


class RdsListItem(MyArray, Item):
    pipeline: str = 'RedisPipeline'
    rds_type: str = 'LIST'
    key: str = None
    __to_json: bool = False

    def __init__(self, initlist: list = None,
                 key: str = None, rds_type: str = None,
                 to_json: bool = False, **kwargs):
        if to_json and initlist.__len__() > 0:
            self.__to_json = to_json
            initlist = list(map(json.dumps, initlist))
        else:
            initlist = initlist
        super().__init__(initlist, **kwargs)
        self.key = key
        self.rds_type = rds_type or self.rds_type

    def append(self, item, to_json=False) -> None:
        """
        :param item: 数据实体
        :param to_json: if to_json is True -> JSON(item)
        :return:
        """
        if self.__to_json:
            item = json.dumps(item, ensure_ascii=False)
        self.data.append(item)


class MysqlItem(dict, Item):
    pipeline: str = 'MySQLPipeline'
    table: str = None

    def __init__(self, initdict=None, table=None, **kwargs):
        if initdict is None:
            initdict = {}
        super().__init__(self, **initdict)
        self.table = table
        for key, val in kwargs.items():
            self.__dict__[key] = val


class MysqlListItem(MyArray, Item):
    pipeline = 'MySQLPipeline'
    table = None
