import os

import ReSpider.setting as setting
from ReSpider.pipelines import BasePipeline
import aiofiles
import csv
from aiocsv import AsyncDictWriter
from ReSpider.extend.item import FileItem, CSVItem, CSVItems


class FilesPipeline(BasePipeline):
    name = 'files_pipeline'

    def __init__(self, spider, **kwargs):
        super().__init__(spider, **kwargs)

    async def process_item(self, item: FileItem, spider):
        file = f'{item.filename}.{item.filetype}'
        data_path = item.data_directory or setting.DATA_PATH
        self.logger.debug(f'{data_path}/{file}')
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        mode = item.mode  # 写入方式
        encoding = item.encoding
        if mode[-1] == 'b':
            encoding = None
        async with aiofiles.open(f'{data_path}{file}', mode=mode, encoding=encoding) as fp:
            await fp.write(item.get('source'))
        return item    # Todo 为了兼容后续版本数据处理的pipeline


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
            filename = item.filename
        file = f'{filename}.{item.filetype}'
        data_path = item.data_directory or setting.DATA_PATH  # item的数据存放路径
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        mode = item.mode  # 写入方式
        fieldnames = item.fieldnames or self._get_fieldnames(item)
        if fieldnames is None or []:
            return item
        async with aiofiles.open(data_path + file, mode=mode, encoding='utf-8', newline='') as afp:
            # if not self.writer:
            self.writer = AsyncDictWriter(afp, fieldnames, restval="NULL", quoting=csv.QUOTE_ALL)
            if self.column_index.get(filename, False) is False:  # 表头是否写入过使用<dict>来存储
                await self.writer.writeheader()
                self.column_index[filename] = True
            if isinstance(item, CSVItems):  # 传入多个item
                await self.writer.writerows(item.get('rows'))
            else:
                await self.writer.writerow(item)
        return item

    def _get_fieldnames(self, item):
        if isinstance(item, CSVItems):
            try:
                fieldnames = item['rows'][0].keys()
            except IndexError:
                self.logger.warning('<CSVItems Type> "rows" Field is Empty')
                return None
        else:
            fieldnames = item.keys()
        return fieldnames

    """
    async def get_file(self, spider):
        # 使用异步的方式打开文件对象
        print(spider.name)
        async with aiofiles.open(f'{spider.name}.csv', 'a+', encoding='utf-8') as fp:
            self.afp = fp
    """
