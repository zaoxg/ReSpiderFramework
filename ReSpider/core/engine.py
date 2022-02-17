# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 22:08
# @Author  : ZhaoXiangPeng
# @File    : engine.py

import asyncio
import time
import ReSpider.setting as setting
from ReSpider.core.observer import Observer
from ReSpider.http import Request
from ReSpider.extend import load_object
from ReSpider.extend import LogMixin
# from ReSpider.extend.item import Item
from ReSpider.core.item import Item
import functools


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
    async def heart_beat(cls):
        await asyncio.sleep(setting.HEART_BEAT_TIME)

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
                        setting.HEART_BEAT_TIME = 60  # 把心跳时间修改为60s
                        self.logger.debug('Continuous Monitoring...')
                        continue
                    else:
                        self.logger.info('Event loop has %s task, Stop running' % tasks.__len__())
                    break
                continue
            await semaphore.acquire()  # 同时只能task_limit个去操作scheduler
            await asyncio.sleep(setting.DOWNLOAD_DELAY or 0)
            task = self.loop.create_task(self._process_request(request, spider, semaphore))
            task.add_done_callback(functools.partial(self._handle_response_output, request, spider))

    async def _process_request(self, request, spider, semaphore):
        try:
            response = await self._process_download(request, spider)
        except Exception as e:
            self.logger.error('Process request %s' % e, exc_info=True)
        else:
            return response
        finally:
            # 释放锁
            semaphore.release()

    async def _process_download(self, request, spider=None):
        """
        把<Request>添加到<Response>
        :param request:
        :param spider:
        :return:
        """
        response = await self.downloader.fetch(request)
        return response

    def _handle_response_output(self, request, spider, future: asyncio.Task):
        """
        处理响应
        :param response:
        :param request:
        :param spider:
        :return:
        """
        response = future.result()
        if isinstance(response, Request):
            # 返回的response是<Request>的话就加到任务队列
            self._add_task(response)
        else:
            self.loop.create_task(self._process_response(response, request, spider))

    async def _process_response(self, response, request, spider):
        """
        使用定义的 callback 处理响应
        :param response:
        :param request:
        :param spider:
        :return:
        """
        async def _process_result(r):
            if r is None:
                pass
            elif isinstance(r, Request):
                # 响应为新的请求, 加入到任务队列
                self._add_task(r)
            elif isinstance(r, Item):
                await self.pipelines.process_chain('process_item', r, spider)
        callback = request.callback or spider.parse
        try:
            callback_result = callback(response)  # 可能返回个生成器(先看看item怎么返回吧)
            if callback_result.__class__.__name__ == 'async_generator':
                async for result in callback_result:
                    await _process_result(result)
            else:
                for result in callback_result:
                    await _process_result(result)
        except TypeError as type_error:  # 捕获 callback结果为空的异常
            if type_error.args[0] == "'NoneType' object is not iterable":
                self.logger.debug(f'Function "{callback.__qualname__}" has no return value')
            else:
                self.logger.error(type_error, exc_info=True)
        except Exception as other_exec:  # 执行回调函数的异常
            # 先不管有什么问题, 请求重新入队列
            if request.retry is True:
                self._add_task(self._set_request_retry(request))
            self.logger.error('spider parse error: %s' % other_exec, exc_info=True)

    def _init_start_request(self, start_requests):
        """
        初始化初始请求<list>
        :param start_requests:
        :return:
        """
        for start_request in start_requests or []:
            self._add_task(request=start_request)

    def _next_request_from_scheduler(self, spider):
        request = self.scheduler.next_request()
        if not request:
            return
        return request

    @classmethod
    def _set_request_retry(cls, req):
        req.retry_times += 1
        return req

    def _add_task(self, request):
        self.scheduler.enqueue_request(request)
