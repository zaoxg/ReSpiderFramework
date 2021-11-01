# -*- coding: utf-8 -*-
# @Time    : 2021/10/7 0:44
# @Author  : ZhaoXiangPeng
# @File    : item.py


class Item:
    # pipeline = None
    # data_directory = None
    # filename = None
    # filetype = None
    # mode = None
    # encoding = None

    def __init__(self, pipeline, **kwargs):
        print(pipeline)
        print(kwargs)
        self.pipeline = pipeline
        self.data_directory = kwargs.get('data_directory')


class FileItem(bytes, Item):
    # pipeline = None
    # data_directory = None
    # filename = None
    # filetype = None
    # mode = None
    # encoding = None

    def __init__(self, arg, **kwargs):
        print(arg)
        print(kwargs)
        pipeline = kwargs.pop('pipeline', 'FilesPipeline')  # 指定 pipelines
        data_directory = kwargs.pop('data_directory') if 'data_directory' in kwargs else None
        filename = kwargs.get('filename')
        filetype = kwargs.get('filetype', '').lower()
        mode = kwargs.get('mode', 'w')  # 文件写入方式, 默认从头开始
        encoding = 'utf-8' or kwargs.get('encoding')
        Item.__init__(self, pipeline, **kwargs)
        bytes.__init__(self, arg)
        # super().__init__()

    @property
    def pipeline(self):
        return 'FilesPipeline'


def Pipeline():
    return 'File'


class Bytes(str):
    str.pipeline = Pipeline
    
    def __init__(self, name):
        super().__init__()
        self.name = name


if __name__ == '__main__':

    b = Bytes('hello')
    b.ppp = 'zhaox'
    print(b.ppp)
    print(b)
    print(b.name)
    # f = FileItem(b'hello world', filename='hw')
    # f.data_directory = 'H:/'
    # print(f)
    # print(f.pipeline)
    # print(f.data_directory)
    # a = {'a': 5}
    # b = a.pop('b') if 'b' in a else None
    # print(b)
    # b = a.get('b')
    # if b:
    #     del a['b']
