# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 9:48
# @Author  : ZhaoXiangPeng
# @File    : metaclass.py

from typing import List
from parsel.selector import SelectorList


class BytesMetaclass(type):
    def __new__(cls, name, bases, attrs, *args, **kwargs):
        attrs['data_directory'] = 'H:/'
        return type.__new__(cls, name, bases, attrs)


class MyBytes(bytes, metaclass=BytesMetaclass):
    pass


class ItemMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        attrs['set_attribute'] = mcs.set_attribute
        return type.__new__(mcs, name, bases, attrs)

    # def __init__(cls, name, bases, namespace, **kwargs):
    #     super().__init__(name, bases, namespace, **kwargs)
    #     if not hasattr(cls, 'registory'):
    #         # this is the base class
    #         cls.registory = {}
    #     else:
    #         # this is the subclass
    #         cls.registory[name.lower()] = cls

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


class DataItems(ArrayItem, Item):
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


def make_item(cls, data: dict):
    """
    @summary: idea form https://github.com/Boris-code/feapder
    提供Item类与原数据，快速构建Item实例
    :param cls: Item类
    :param data: 字典格式的数据
    """
    item = cls()
    for key, val in data.items():
        setattr(item, key, val)
    return item


class TestItem:
    data_directory = 'a'


class BytesItem(bytes, TestItem):
    x = ''


if __name__ == '__main__':
    a = make_item(TestItem, {'tag': 'test'})
    li = CSVItem({'序号': '1', '出版年': '2018', '副书名': '', '丛书名': '西北师范大学外国语言文学文库', '分册（辑）名': '', '责任者': '杨保林', 'ISBN': '978-7-03-057928-7', '主题词': '小说研究－澳大利亚－现代', '丛书责任者': '', '内容提要': '澳大利亚旅亚小说作为世界旅行文学研究的一部分引起了研究者的关注。越南战争结束之后，许多澳大利亚主流作家先后创作了一大批以亚洲为背景或者以亚洲旅行为主题的小说。澳大利亚当代旅亚小说较全面地反映了澳大利亚当代人对亚洲国家和人民的新看法，从这些旅亚小说中不难看出当代澳大利亚人对自身的民族身份定位。澳大利亚当代旅亚小说从总体上分为两个阶段，六七十年代”转向亚洲”阶段的澳大利亚旅亚小说展示了澳大利亚主流社会刚刚把目光转向亚洲时对亚洲既热衷又恐惧的复杂情感，八九十年代”拥抱亚洲”阶段的澳大利亚旅亚小说反映了澳大利亚人一方面日益希望拥抱亚洲的愿望。本书选取当代澳大利亚文坛四位主流（英裔白人男性）作家的四部旅亚小说进行研究，考察当代澳大利亚旅亚小说在亚洲表征以及自我身份定位方面经历的变化。', 'book_id': 'b05044569'})
    # li.set_attribute(collection='data_cnki_tsyz')
    print(li)
    lis = CSVListItem([{'序号': '1', '出版年': '2018', '副书名': '', '丛书名': '西北师范大学外国语言文学文库', '分册（辑）名': '', '责任者': '杨保林',
                       'ISBN': '978-7-03-057928-7', '主题词': '小说研究－澳大利亚－现代', '丛书责任者': '',
                       '内容提要': '澳大利亚旅亚小说作为世界旅行文学研究的一部分引起了研究者的关注。越南战争结束之后，许多澳大利亚主流作家先后创作了一大批以亚洲为背景或者以亚洲旅行为主题的小说。澳大利亚当代旅亚小说较全面地反映了澳大利亚当代人对亚洲国家和人民的新看法，从这些旅亚小说中不难看出当代澳大利亚人对自身的民族身份定位。澳大利亚当代旅亚小说从总体上分为两个阶段，六七十年代”转向亚洲”阶段的澳大利亚旅亚小说展示了澳大利亚主流社会刚刚把目光转向亚洲时对亚洲既热衷又恐惧的复杂情感，八九十年代”拥抱亚洲”阶段的澳大利亚旅亚小说反映了澳大利亚人一方面日益希望拥抱亚洲的愿望。本书选取当代澳大利亚文坛四位主流（英裔白人男性）作家的四部旅亚小说进行研究，考察当代澳大利亚旅亚小说在亚洲表征以及自我身份定位方面经历的变化。',
                       'book_id': 'b05044569'}])
    # if isinstance()
    f = IoItem(b'hello world')
    print(f)
    s = FileItem('hello world')
    print(s)
    f.m = 'b'

    b = MyBytes(b'hello world')
    b.a = 'c'
    print(b)
    print(b.data_directory)
