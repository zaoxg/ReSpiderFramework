# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 9:48
# @Author  : ZhaoXiangPeng
# @File    : metaclass.py

from typing import List
from collections import UserList


class BytesMetaclass(type):
    def __new__(cls, name=None, bases=None, attrs=None, *args, **kwargs):
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


class Item:
    __dict__ = {}
    pass


class ArrayItem(UserList):
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


class BytesItem:
    data: bytes = None

    def __init__(self, initbytes=None, **kwargs):
        if initbytes is not None:
            self.data = initbytes
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def __repr__(self): return repr(self.data)

    def hex(self, sep=None, bytes_per_sep=None):
        if isinstance(self.data, bytes):
            return self.data.hex(sep, bytes_per_sep)

    def decode(self, encoding='utf-8', errors='strict'):
        return self.data.decode(encoding, errors)


class DataItem(dict, Item):
    pipeline = 'MongoDBPipeline'
    collection = None

    def set_attribute(self, collection, **kwargs):
        self.collection = collection


class DataListItem(UserList, Item):
    pipeline = 'MongoDBPipeline'
    collection = None

    def __init__(self, initlist=None, collection=None, **kwargs):
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
        self.collection = collection

    def set_attribute(self, collection, **kwargs):
        self.collection = collection


class DataItems(ArrayItem, Item):
    pipeline = 'MongoDBPipeline'
    collection = None

    def set_attribute(self, collection, **kwargs):
        self.collection = collection


class IoItem(BytesItem, Item):
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

    def __init__(self, arg, **kwargs):
        self.__dict__ = kwargs or {}
        super().__init__(self, **arg)

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
    fieldnames = None

    # def __init__(self, arg, *args, **kwargs):
    #     self.__dict__ = kwargs or self.__dict__
    #     super().__init__(self, *arg)
    #     super(CSVListItem, self).__dict__ = kwargs
    #     super(list, self).__init__(*arg)

    def set_attribute(self,
                      data_directory=None,
                      filename=None,
                      mode=None,
                      encoding=None,
                      fieldnames=None, **kwargs):
        self.data_directory = data_directory
        self.filename = filename
        self.mode = mode
        self.encoding = encoding or self.encoding
        self.fieldnames = fieldnames or self[0].keys() if len(self) else []


class I:
    pass


class RdsItem(dict, Item):
    pipeline: str = 'RedisPipeline'
    rds_type: str = 'LIST'
    key: str = None

    def __init__(self, arg=None, **kwargs):
        if arg is None:
            arg = {}
        self.__dict__ = kwargs or self.__dict__
        super().__init__(self, **arg)

    # def __getattribute__(self, item):
    #     value = object.__getattribute__(self, item)
    #     # if item in self.keys():
    #     #     return self[item]
    #     return value

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
    pass


if __name__ == '__main__':
    # rds_item = RdsItem({"SID": "201236", "Ecp_ClientId": "4220211130501371135"}, key='cnki_tsyzsjk:cookies_pool', rds_type='SET')
    # # # rds_item.update({"ASP.NET_SessionId": "4okmi1xltj4texpgif0wwsec", "SID": "201236", "Ecp_ClientId": "4220211130501371135", "LID": "WEEvREcwSlJHSldSdmVqeVpQZi9LZ3VBNFdSU0hkOCtFUEpCNnpJbjJvZz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!", "Ecp_IpLoginFail": "", ".ASPXAUTH": "91CD1BC4EF747A6E4F0764F1D7BEF9D7CF9635297A89A15487D11C24D91A9A4049CCBE906785EF0356FB34AA96DA79E987A135950C6B37CA37EEF6BD0D95C45C091F50304DEB663DD4B575AA00E174533064CAC1827BA5B3AF152FFAF20531DDCAD5D8C9181B3796F09F8C68D11BC5A0DFE3BD289DB8E7496DDCB542F94D362B8682EB178D2E1DA86E9F76E61E553A0DE0CA2634A5F3ADA1883990F783439D99D67B0265274B025FAF54A081A38AFFD84684B473195B4F5277DE4C016578A8E02ECE236A17A34343973F07383DCA1A583EFBCE802D4E334924A5A5F3B619879E63DA01172FCE5C6B0A69565662807C3911716D051E07F0566C6C7835916BF0BAFACE0A34BBE4048AF13DD99AF7381A8CE6C8093F3BC165B959CAD79BCB91358BABD01A14E61A882914CD082D713AE57E6643C34D14A2937F1F210063A815A51D2FF21E9FA7C51B4C810FC26E787E6A98B42C861CFE06547278C62324B3FA26FE91AE6FA2060C5426AE49D2C0F30D2F6270634243CA24515AE0AC2213A4FC90DDB277DFF5E08FE56DB39B5A7FFBE42409B9EA0381775EFB71115C4E335127AD5616928400D7EDB8C8629B21F46B1060C3B798C28EDD695EC5AEB0B6A3B48CAEF4EA69AFA4CE56E92B719A357F4F8479B9AAEBC7B01FF4C5C9DA92367B924D67D2A8D9271647ACA5B3E719A729678C1F5C71A35F306525E69E1BD37244E2F85550027A988322B31718E8BFB67EF72608F711BAF5D720408A9EFCAD514C25FAA2C9515DDBDA041EA17315FFA84DD68119040B052636B46F0DF87DB604B7A309FF8458CC55BF9482B2358C32FE32E50C9C7BEC24F9AEBAC97E762172824DAFB4C09475D10CE1328BAE043097F45EA436B57C3E2781669DB5CCB44745E8C7EB103F6B6513ED636F84130C0FFACC015DEF54299558351D72C0D90C1BEDF8D35666259399CAA84ED31CA1DC4AF156626FD45164650FCA29C316D21AF9C32F52EA761C6EE0265D4E04BAE33383D5D9E9E7C439AF1516DFB799B01A28F335E05F8D90079F7613D5DE4790E1A72985C26F4E9613C61B53CB2F1A12458DF3EC4241F735839B9764452471F5DADAA46A6C4C11E9212B5B5C0D3560EB288ADC653D886B9E315779399B7FE011597716E52EAD0DDDD31BB432789EBC9DCA1CDE09EF49B9EA0D21FF817E4401FD3BEFBFCC8DF11EC004FF00EF24AE82905954929023A4FC2181BA0F950B60D341A9A8204C11A1F7CC6FEABF60BD3FE996F6426078BC09CAD291DF55E7198ECD3DA3BFE351950913D6588F1788429C99A30FBC17EBF7855FE035CB558810580BA2514C4CBB0840C46D2377A00F48FE6D018AE3AD910CDBC755A2D321DD216191593A2E22B0979731ABE854B11828B4027745C8AD3924874CE184A0C7F7991FA32080F6B5093DED5358E5ADDC84A945F3852EB8B073E6923CFB574800EE2E0C9CACDCEA9702CF322EEB75E1F699D324329F704A4470A6D5E315EE3327FBA1133EDD3F2C310196DFFDCD4D9315844502EB259CA52AD2F1D28D7FC02BD9A3DCCCC44CD137E5E76AE97C192EC36C075C5AD32EDB21A16F41BEC83EC869943B40DE1A11F95CEA5EF67B822A4A42D0B30BF621D3365FCBC59F1ECA9E6FD027BD3CF249CB1975EFD0E7FE6560B14DA033BC8BA0FC6E7260599E10B32A24EA68C767446E962B42F9F668AE3D4929239F9153DD638952651BDEFA05002DCF0FDAAA860E24CE2C644CD2B17FA2D9970417AA2FDE4B1664446E7522C855C850E9144BB447499CCAB2CCEB491CBE9B042A12D1E326737A7074384CB1E0F0C4890D69D87E9A88ADC06C589052A14E9E36362EF930F777A49355CEFFB5872DE2CD20B776A3EDA47B9AAE7104D6FC6515F03ADFA08685040425C9EAA06EAA466EAEE0BB15525FE01C81A909F1956ED79348C43DC1EA01B4EE803F3E0924591FF719203BE48285A035F111BB72F4E19C47632E5DEAC7874BE9564B3E51A70A7DD1778D36B87033745C5FCB4B0A5AA3D81C4087817F1E4467EC8871672E05E73CDE4282414A3A726CA29652E385E5BF04D08E39AA841D5E02F3CDDECC4D2D90E9A97ABB173BB770750A6AC049245E20516493C1C8660AE56BA30C7B517FB99AE3C059927188302D4CE98F52987B5CCBE4AC56CBF9096F1293D93A6CE5A49A75C70CB56C4CF312EB7501ED04F6382B1E8A168A17211C367C1DFC932F815921D21E3F9462AD9D8CE25F10839DD3FBDBD2C0CEAE75926474B474ECD5EE4F5CFA7194393EDB9BD136579DB91D0414B2D4CA131B79CAA7B855AFA450BF69E06A9C2C3DFAE5530D65D422E8D3C2B147DF2A2528E85EA299DA3C4A4DF0EF37239C668E83A3E3AA7C1CCE13D6C95253A5CECF6446CC6676", "__RequestVerificationToken": "L6EXI4alT4_t5E4iKfcuzsgLav93d_GsACzeRoo8uA1ueQRw0LyWBv4uya42rRG9bhmmMHn5yBRbuGEEAU6NmVknPlRJoyb65VDPhvpy5G01"})
    # # print(rds_item.SID)
    # li = CSVItem({'序号': '1', '出版年': '2018', '副书名': '', '丛书名': '西北师范大学外国语言文学文库', '分册（辑）名': '', '责任者': '杨保林', 'ISBN': '978-7-03-057928-7', '主题词': '小说研究－澳大利亚－现代', '丛书责任者': '', '内容提要': '澳大利亚旅亚小说作为世界旅行文学研究的一部分引起了研究者的关注。越南战争结束之后，许多澳大利亚主流作家先后创作了一大批以亚洲为背景或者以亚洲旅行为主题的小说。澳大利亚当代旅亚小说较全面地反映了澳大利亚当代人对亚洲国家和人民的新看法，从这些旅亚小说中不难看出当代澳大利亚人对自身的民族身份定位。澳大利亚当代旅亚小说从总体上分为两个阶段，六七十年代”转向亚洲”阶段的澳大利亚旅亚小说展示了澳大利亚主流社会刚刚把目光转向亚洲时对亚洲既热衷又恐惧的复杂情感，八九十年代”拥抱亚洲”阶段的澳大利亚旅亚小说反映了澳大利亚人一方面日益希望拥抱亚洲的愿望。本书选取当代澳大利亚文坛四位主流（英裔白人男性）作家的四部旅亚小说进行研究，考察当代澳大利亚旅亚小说在亚洲表征以及自我身份定位方面经历的变化。', 'book_id': 'b05044569'}, data_directory='D:/')
    # # li.set_attribute(collection='data_cnki_tsyz')
    # print(li)
    # lis = CSVListItem([{'序号': '1', '出版年': '2018', '副书名': '', '丛书名': '西北师范大学外国语言文学文库', '分册（辑）名': '', '责任者': '杨保林',
    #                    'ISBN': '978-7-03-057928-7', '主题词': '小说研究－澳大利亚－现代', '丛书责任者': '',
    #                    '内容提要': '澳大利亚旅亚小说作为世界旅行文学研究的一部分引起了研究者的关注。越南战争结束之后，许多澳大利亚主流作家先后创作了一大批以亚洲为背景或者以亚洲旅行为主题的小说。澳大利亚当代旅亚小说较全面地反映了澳大利亚当代人对亚洲国家和人民的新看法，从这些旅亚小说中不难看出当代澳大利亚人对自身的民族身份定位。澳大利亚当代旅亚小说从总体上分为两个阶段，六七十年代”转向亚洲”阶段的澳大利亚旅亚小说展示了澳大利亚主流社会刚刚把目光转向亚洲时对亚洲既热衷又恐惧的复杂情感，八九十年代”拥抱亚洲”阶段的澳大利亚旅亚小说反映了澳大利亚人一方面日益希望拥抱亚洲的愿望。本书选取当代澳大利亚文坛四位主流（英裔白人男性）作家的四部旅亚小说进行研究，考察当代澳大利亚旅亚小说在亚洲表征以及自我身份定位方面经历的变化。',
    #                    'book_id': 'b05044569'}], data_directory='D:/')
    # print(lis)
    # lis.set_attribute(data_directory='D:/')
    f = IoItem(b'hello world', data_directory='D:/')
    print(f)
    # s = FileItem('hello world')
    # print(s)
    # f.m = 'b'
    #
    # b = MyBytes(b'hello world')
    # b.a = 'c'
    # print(b)
    # print(b.data_directory)
