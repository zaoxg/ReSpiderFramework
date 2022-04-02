# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 22:08
# @Author  : ZhaoXiangPeng
# @File    : engine.py

import asyncio
import time
from typing import AsyncGenerator, Generator, Coroutine
import ReSpider.setting as setting
from ReSpider.core.observer import Observer
from ReSpider.http import Request, Response
from ReSpider.extend.misc import load_object
from ReSpider.extend.logger import LogMixin
from ReSpider.item import Item
import ReSpider.utils.tools as tools
from ReSpider.core.spiders import Crawler


class Core:

    async def single_flow(self, request: Request, spider: Crawler, semaphore):
        # 获取任务
        # 处理请求
        # 发送请求
        # 处理响应
        # 处理callback
        response = await self.process_request(request, spider)
        semaphore.release()  # 释放锁
        if response:
            await self.process_response(request, response, spider)

    async def next_request(self):
        """从任务队列获取一个请求, 需重写"""
        raise NotImplementedError

    async def process_request(self, request: Request, spider: Crawler):
        raise NotImplementedError

    async def process_response(
            self,
            request: Request, response: Response, spider: Crawler = None):
        """
        统一处理 Response, 成功进入正常的处理流程, 否则到处理异常请求的流程
        :param request: 请求, 如果是异常响应, 需要把请求重新入队列
        :param response: <Response>
        :param spider: <Spider>, 部分组件需要使用spider的属性
        :return:
        """
        if response:
            await self.process_succeed_response(
                request, response, spider
            )
        else:
            await self.process_failed_response(
                request, response, spider)

    async def process_succeed_response(
            self,
            request: Request, response: Response,
            spider: Crawler = None):
        """
        使用定义的 callback 处理响应
        :param response: success Response
        :param request:
        :param spider:
        :return:
        """
        if request.callback:
            callback = (
                request.callback
                if callable(request.callback)
                else tools.get_method(spider, request.callback)
            )
        else:
            callback = spider.parse

        try:
            callback_result = callback(response)  # 返回一个生成器

            if isinstance(callback_result, AsyncGenerator):
                async for result in callback_result:
                    await self.process_callback_result(result, spider)
            elif isinstance(callback_result, Generator):
                for result in callback_result:
                    await self.process_callback_result(result, spider)
            elif isinstance(callback_result, Coroutine):
                pass
            else:
                pass

        except Exception as exception:
            await self.handle_callback_error(request, exception, spider)

    async def process_failed_response(
            self, request: Request, response: Response,
            spider: Crawler = None):
        """
        处理失败的响应, 需要重写
        :param request:
        :param response: 失败的 Response
        :param spider:
        :return:
        """
        pass

    async def process_callback_result(
            self, callback_result, spider: Crawler):
        """
        处理回调函数的结果, 上一层是一个循环
        :param callback_result: 回调函数的返回结果
        :param spider:
        :return:
        """
        if callback_result is None:
            pass
        elif isinstance(callback_result, Request):
            # 响应为新的请求, 加入到任务队列
            await self.handle_callback_request(
                callback_result
            )

        elif isinstance(callback_result, Item):
            await self.handle_callback_item(
                callback_result, spider
            )

        elif isinstance(callback_result, Response):
            pass

    async def handle_callback_request(self, request: Request):
        raise NotImplementedError

    async def handle_callback_item(self, item: Item, spider):
        raise NotImplementedError

    async def handle_callback_error(self, request: Request, exception: Exception, spider: Crawler = None):
        raise NotImplementedError


class Engine(Core, LogMixin):
    observer = Observer()

    def __init__(self, spider):
        super().__init__(spider)
        self.logger.info('ENGINE START INIT ...')
        self.spider = spider
        self.loop = self.observer.loop

        self.scheduler = load_object(
            setting.SCHEDULER).from_crawler(spider, observer=self.observer)
        self.downloader = load_object(
            setting.DOWNLOADER).from_crawler(spider, observer=self.observer)
        self.pipelines = load_object(
            setting.PIPELINE_MANAGER).from_crawler(spider, observer=self.observer)

        self.logger.info('ENGINE INIT SUCCESS.')

    def start(self):
        self.observer.engine_status = 'START'
        start_time = time.time()
        self.logger.info('IT\'S EXCELLENT. IT\'S FLEXIBLE ...')
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
            self.loop.run_until_complete(
                # 运行住流程, 由主流程创建单一任务
                self.start_master_flow(spider)
            )
        except Exception as e:
            self.logger.error('[execute] %s' % e, exc_info=True)
        finally:
            self.loop.run_until_complete(
                self.loop.shutdown_asyncgens())
            self.loop.stop()
            self.logger.info('THE END.')

    @classmethod
    async def heart_beat(cls):
        await asyncio.sleep(setting.HEART_BEAT_TIME)

    async def start_master_flow(self, spider):
        """
        不断的获取请求
        :param spider:
        :return:
        """
        task_limit = setting.TASK_LIMIT or setting.CONCURRENT_REQUESTS
        semaphore = asyncio.Semaphore(value=task_limit)
        while True:
            request = await self.next_request()
            if request is None:
                await self.heart_beat()
                tasks = asyncio.all_tasks(self.loop)
                self.logger.debug(
                    f'Not has new request, Current Event loop has %s task.' % tasks.__len__())

                if not self.scheduler.has_pending_requests() and len(tasks) <= 1:
                    if setting.ALWAYS_RUNNING is True:
                        setting.HEART_BEAT_TIME = 60  # 把心跳时间修改为60s
                        self.logger.debug('Continuous Monitoring...')
                        continue
                    else:
                        self.logger.info(
                            'Event loop has %s task, Stop running' % tasks.__len__())
                    break
                continue
            await semaphore.acquire()  # 同时只能task_limit个去操作scheduler
            await asyncio.sleep(setting.DOWNLOAD_DELAY or 0)
            # 创建一个任务
            self.loop.create_task(
                self.single_flow(
                    request, spider, semaphore)
            )

    async def _process_download(self, request: Request, spider=None):
        """
        下载请求,
        :param request:
        :param spider:
        :return: Response or Request
        """
        response = await self.downloader.fetch(request)
        return response

    def _init_start_request(self, start_requests):
        """
        初始化初始请求<list>
        :param start_requests:
        :return:
        """
        for start_request in start_requests or []:
            self._add_task_to_scheduler(request=start_request)

    @classmethod
    def _set_request_retry(cls, req: Request) -> Request:
        req.retry_times += 1
        return req

    def _add_task_to_scheduler(self, request):
        self.scheduler.enqueue_request(request)

    async def next_request(self) -> Request:
        request = await self.scheduler.next_request()
        return request

    async def process_request(
            self, request: Request, spider) -> Response:
        """返回值必须是 <Response>
        在处理请求时 出现异常 或 处理后非<Response> 返回的是 <Request>
        """
        response_result = None
        try:
            response_result = await self._process_download(request, spider)
        except Exception as e:
            spider.logger.warning('Process request: %s' % e, exc_info=True)
            self._add_task_to_scheduler(request)  # 下载出错时任务重新加入队里
        else:
            if isinstance(response_result, Response):
                return response_result
        self._add_task_to_scheduler(request)

    async def handle_callback_item(self, item: Item, spider):
        """处理回调函数返回的Item, 重写"""
        await self.pipelines.process_chain(
            'process_item', item, spider
        )

    async def handle_callback_request(self, request: Request):
        """处理回调函数返回 Request
        加入任务队列, （Todo 也许需要立马执行而不入队列）
        """
        self._add_task_to_scheduler(request)

    async def handle_callback_error(self, request: Request, exception: Exception, spider=None):
        """处理异常回调, 错误统一处理, 入需重试则入队列"""
        if isinstance(exception, TypeError):
            self.logger.error(exception, exc_info=True)
        elif isinstance(exception, NotImplementedError):
            self.logger.warning(exception)
            raise exception
        else:
            if request.retry:
                self._add_task_to_scheduler(
                    self._set_request_retry(request))
            spider.logger.error(exception, exc_info=True)

    async def process_failed_response(
            self, request: Request, response: Response,
            spider=None):
        """处理错误(失败)的响应"""
        self._add_task_to_scheduler(request)
