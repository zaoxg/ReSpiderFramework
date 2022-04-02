import os
import re
import ReSpider.setting as setting
from ReSpider.pipelines import BasePipeline
from ReSpider.item import CSVListItem, CSVItem, FileItem
import aiofiles
import csv
from aiocsv import AsyncDictWriter


class FilePipeline(BasePipeline):
    name = 'file_pipeline'

    def __init__(self, spider, **kwargs):
        super().__init__(spider, **kwargs)

    async def process_item(self, item: FileItem, spider):
        item.filename = re.sub(r'[\\/:*?"<>|]', '`', str(item.filename))
        file: str = f'{item.filename}.{item.filetype}'
        data_path: str = item.data_directory or setting.DATA_PATH
        self.logger.debug(f'{data_path}/{file}')
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        mode = item.mode  # 写入方式
        encoding = item.encoding
        if mode[-1] == 'b':
            encoding = None
        async with aiofiles.open(f'{data_path}/{file}', mode=mode, encoding=encoding) as fp:
            await fp.write(item.data)
        return item


class CSVPipeline(BasePipeline):
    name = 'csv pipeline'

    def __init__(self, spider, **kwargs):
        super().__init__(spider, **kwargs)
        self.column_index = dict()
        self.writer = False
        self.head = []

    async def process_item(self, item: CSVItem, spider):
        filename = spider.name
        if item.filename:
            filename = re.sub(r'[\\/:*?"<>|]', '`', str(item.filename))
        file = f'{filename}.{item.filetype}'
        data_path = item.data_directory or setting.DATA_PATH  # item的数据存放路径
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        mode = item.mode  # 写入方式
        fieldnames = item.fieldnames or self._get_fieldnames(item)
        if fieldnames is None or []:
            return item
        async with aiofiles.open(data_path + '/' + file, mode=mode, encoding='utf-8', newline='') as afp:
            # if not self.writer:
            self.writer = AsyncDictWriter(afp, fieldnames, restval="NULL", quoting=csv.QUOTE_ALL)
            if self.column_index.get(filename, False) is False:  # 表头是否写入过使用<dict>来存储
                await self.writer.writeheader()
                self.column_index[filename] = True
            if isinstance(item, CSVListItem):
                await self.writer.writerows(item)
            else:
                await self.writer.writerow(item)
        return item

    def _get_fieldnames(self, item):
        if not item.fieldnames:
            try:
                fieldnames = item[0].keys()
            except IndexError:
                self.logger.warning('<CSVItems Type> "rows" Field is Empty')
                return None
        else:
            fieldnames = item.fieldnames
        return fieldnames

    """
    async def get_file(self, spider):
        # 使用异步的方式打开文件对象
        print(spider.name)
        async with aiofiles.open(f'{spider.name}.csv', 'a+', encoding='utf-8') as fp:
            self.afp = fp
    """
