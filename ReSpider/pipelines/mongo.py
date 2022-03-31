import ReSpider.setting as setting
from . import BasePipeline
from ..db.mongodb import AsyncMongoDB as MongoDB
from ..core.item import DataListItem, DataItem

__all__ = [
    "MongoPipeline"
]


class MongoPipeline(BasePipeline):
    name = 'mongodb pipeline'

    def open_spider(self, spider=None, **kwargs):
        if setting.MONGODB_URL:
            self._db = MongoDB.from_url(setting.MONGODB_URL, loop=self._observer.loop)
        else:
            self._db = MongoDB(loop=self._observer.loop)

    async def process_item(self, item: DataItem, spider):
        if not item:  # 先检查一下
            return item
        collection = item.collection
        if isinstance(item, DataListItem):
            add_count = await self._db.add_batch(collection, item)
        else:
            add_count = await self._db.add(collection, item)
        if add_count:
            self.logger.info('入库 %s 行数 %s 条, 影响行数 %s 条' % (collection, len(item), add_count))
        return item  # Todo 为了兼容后续版本数据处理的pipeline
