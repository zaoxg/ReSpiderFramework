from . import BasePipeline
from ..extend.item import DataItem
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError


class MongoDBPipeline(BasePipeline):
    name = 'mongodb pipeline'

    def __init__(self, spider, **kwargs):
        super().__init__(spider, **kwargs)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        settings = spider.settings
        cls.mongodb_host = settings.get('MONGODB_HOST')
        cls.mongodb_port = settings.get('MONGODB_PORT')
        cls.mongodb_db = settings.get('MONGODB_DB')
        return cls(spider, **kwargs)

    def open_spider(self, spider=None, **kwargs):
        loop = self._observer.loop
        self._clint = AsyncIOMotorClient(self.mongodb_host, self.mongodb_port, io_loop=loop)
        self._db = self._clint[self.mongodb_db]

    async def process_item(self, item: DataItem, spider):
        collection = item.collection
        try:
            await self._db[collection].insert_one(item)
        except DuplicateKeyError:
            self.logger.info('%s error with %s' % (self.name, DuplicateKeyError))
        # except Exception as e:
        #     self.logger.info('%s error with %s' % (self.name, e))
        else:
            return item
        return item  # Todo 为了兼容后续版本数据处理的pipeline
