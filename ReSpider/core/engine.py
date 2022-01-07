import asyncio
import time
import ReSpider.setting as setting
from .observer import Observer
from ..http import Request
from ..extend import load_object
from ..extend import LogMixin
from ..extend.item import Item


class Engine(LogMixin):
    observer = Observer()

    def __init__(self, spider):
        super().__init__(spider)
        self.logger.info('ENGINE START INIT ...')
        self.spider = spider
        # self.settings = spider.settings

        self.scheduler = load_object(setting.SCHEDULER).from_crawler(spider, observer=self.observer)
        self.downloader = load_object(setting.DOWNLOADER).from_crawler(spider, observer=self.observer)
        self.pipelines = load_object(setting.PIPELINE_MANAGER).from_crawler(spider, observer=self.observer)
        self.loop = self.observer.loop
        self.logger.info('ENGINE INIT SUCCESS.')

    def start(self):
        self.observer.engine_status = 'START'
        start_time = time.time()
        self.logger.info('IT\'S EXCELLENT. IT\'S FLEXIBLE ...')
        # self.pipelines.open_spider()
        start_requests = self.spider.start_requests()
        self.execute(self.spider, start_requests)
        self.observer.engine_status = 'STOP'
        self.logger.info(f'RUNNING TIME ({int(time.time() - start_time)}) SECONDS.')
        self.logger.debug('及 其 优 秀 ,  弹 性 很 足.')

    def execute(self, spider, start_requests):
        """
        执行方法
        :param spider:
        :param start_requests:
        :return:
        """
        # 把 starts_requests 加入调度器队列
        self._init_start_request(start_requests)
        self.logger.info('TASK INIT SUCCESS.')
        try:
            self.loop.run_until_complete(self._next_request(spider))
        except Exception as e:
            self.logger.error('[execute] %s' % e, exc_info=True)
            # print('execute ', e)
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            # self.loop.close()
            self.loop.stop()
            self.logger.info('THE END.')

    @classmethod
    async def heart_beat(cls, slp=3):
        await asyncio.sleep(slp)

    async def _next_request(self, spider):
        """
        不断的获取请求
        :param spider:
        :return:
        """
        task_limit = setting.TASK_LIMIT or setting.CONCURRENT_REQUESTS
        semaphore = asyncio.Semaphore(value=task_limit)
        while True:
            request = await self.scheduler.next_request()
            if request is None:
                await self.heart_beat()
                tasks = asyncio.all_tasks(self.loop)
                self.logger.debug(f'Not has new request, Current Event loop has %s task.' % tasks.__len__())
                """
                # Todo
                for t in tasks:
                # self.logger.info('Before Event loop is Null %s ' % t.get_core().__name__)
                    if t.get_coro().__name__ != '_next_request':
                        try:
                            t.cancel()
                        except RuntimeWarning:
                            pass
                """
                # print(tasks)
                if not self.scheduler.has_pending_requests() and len(tasks) <= 1:
                    if setting.ALWAYS_RUNNING is True:
                        self.logger.debug('Continuous Monitoring...')
                        continue
                    break
                continue
            await semaphore.acquire()  # 同时只能task_limit个去操作scheduler
            await asyncio.sleep(setting.DOWNLOAD_DELAY or 0)
            self.loop.create_task(self._process_request(request, spider, semaphore))

    async def _process_request(self, request, spider, semaphore):
        try:
            response = await self._process_download(request, spider)
        except Exception as e:
            self.logger.error('Process request %s' % e, exc_info=True)
            return
        else:
            await self._handle_response_output(response, request, spider)
        # 释放锁
        semaphore.release()

    async def _process_response(self, response, request, spider):
        """
        todo
        :param response:
        :param request:
        :param spider:
        :return:
        """
        callback = request.callback or spider.parse
        result = callback(response)  # 可能返回个生成器(先看看item怎么返回吧)
        if result:
            async for res in result:
                if res is None:
                    continue
                elif isinstance(res, Request):
                    # self.logger.info('[request] %s' % res)
                    self.add_task(res)
                elif isinstance(res, Item):
                    # if 'pipelines' in res.keys():  # 这个似乎是为了兼容比较早的代码做的
                    #     pipeline = res.pop('pipelines', 'pipelines')
                    #     await self.__dict__[pipeline].process_item(res, spider)
                    #     continue
                    await self.pipelines.process_chain('process_item', res, spider)
        else:
            self.logger.debug(f'Function "{callback.__qualname__}" has no return value')

    async def _process_download(self, request, spider):
        """
        把<Request>添加到<Response>
        :param request:
        :param spider:
        :return:
        """
        response = await self.downloader.fetch(request)
        # print(response)
        return response

    async def _handle_response_output(self, response, request, spider):
        """
        处理响应
        :param response:
        :param request:
        :param spider:
        :return:
        """
        if isinstance(response, Request):
            # 返回的response是<Request>的话就加到任务队列
            self.add_task(response)
        else:
            await self._process_response(response, request, spider)

    def _init_start_request(self, start_requests):
        """
        初始化初始请求<list>
        :param start_requests:
        :return:
        """
        for start_request in start_requests or []:
            self.add_task(request=start_request)

    def _next_request_from_scheduler(self, spider):
        request = self.scheduler.next_request()
        if not request:
            return
        return request

    def add_task(self, request):
        self.scheduler.enqueue_request(request)
