# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 18:00
# @Author  : ZhaoXiangPeng
# @File    : item.py


class Item(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class FileItem(Item):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.pipeline = 'FilesPipeline'  # 指定 pipelines
        self.data_directory = kwargs.get('data_directory')
        self.filename = kwargs.get('filename')
        self.filetype = kwargs.get('filetype', '').lower()
        self.mode = kwargs.get('mode', 'w')  # 文件写入方式, 默认从头开始
        self.encoding = 'utf-8' or kwargs.get('encoding')


class CSVItem(Item):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.pipeline = 'CSVPipeline'  # 指定 pipelines
        self.data_directory = kwargs.get('data_directory')
        self.filename = kwargs.get('filename')
        self.filetype = 'csv'
        self.mode = kwargs.get('mode', 'a')  # 文件写入方式, 默认从结束开始
        if kwargs.get('fieldnames') is None:
            assert ValueError('Field "fieldnames" Cannot be empty')
        self.fieldnames = kwargs.get('fieldnames')


class CSVItems(CSVItem):
    """
    dict数组
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RdsItem(Item):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.pipeline = 'RedisPipeline'
        self.rds_type = kwargs.get('rds_type', 'LIST').upper()  # string, set
        self.keys = kwargs.get('keys')


class DataItem(Item):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.pipeline = 'MongoDBPipeline'  # 指定 pipelines
        self.collection = kwargs.get('collection')


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


class It:
    pass


class Items(list, It):
    def __init__(self, arg, *args, **kwargs):
        super().__init__(arg)
        self._ = 'ITEMS'
        self.a = kwargs.get('a')
        self.b = kwargs.get('b')


class ItemData(dict, It):
    def __init__(self, arg, *args, **kwargs):
        super().__init__(arg)
        self._ = 'ITEMDATA'
        self.a = kwargs.get('a')
        self.b = kwargs.get('b')


if __name__ == '__main__':

    i = Items([5, 6, 7, 4], a=1, b='k')
    print(i)
    print(i.a)
    print(i.__class__)
    print(isinstance(i, list))

    d = ItemData({}, a=143, b='j')
    print(d)
    d.update(a=5)
    d.update(l=7)
    print(d)
