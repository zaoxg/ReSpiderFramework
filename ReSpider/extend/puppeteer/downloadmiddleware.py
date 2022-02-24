# -*- coding: utf-8 -*-
# @Time    : 2021/1/24 21:22
# @Author  : ZhaoXiangPeng
# @File    : downloadmiddleware.py
"""
puppeteer组件
使用puppeteer渲染动态网页
在下载器中间件使用
"""

import asyncio
from ..puppeteer import PuppeteerRequest
from ..puppeteer import PuppeteerResponse
import ReSpider.setting as setting
from ReSpider.middlewares import BaseMiddleware
from urllib.parse import urlsplit

from pyppeteer import launch, errors
from .settings import *


class PuppeteerMiddleware(BaseMiddleware):
    def __init__(self, spider, **kwargs):
        super().__init__(spider, **kwargs)
        self.browser = None
        self.BROWSER_OPENED = None

    def open_spider(self, spider=None, **kwargs):
        loop = self._observer.loop
        task = loop.create_task(self.getBrowser())
        loop.run_until_complete(task)

    def close_spider(self, spider=None, **kwargs):
        loop = self._observer.loop or asyncio.get_event_loop()
        task = loop.create_task(self._close_browser())
        loop.run_until_complete(task)

    @classmethod
    def from_crawler(cls, spider, **kwargs):
        settings = setting.PUPPETEER_SETTING
        # cls.headless = None
        # init settings
        cls.window_width = settings.get('PUPPETEER_WINDOW_WIDTH', PUPPETEER_WINDOW_WIDTH)
        cls.window_height = settings.get('PUPPETEER_WINDOW_HEIGHT', PUPPETEER_WINDOW_HEIGHT)
        cls.headless = settings.get('PUPPETEER_HEADLESS', PUPPETEER_HEADLESS)  # 无头
        cls.dumpio = settings.get('PUPPETEER_DUMPIO', PUPPETEER_DUMPIO)
        cls.ignore_https_errors = settings.get('PUPPETEER_IGNORE_HTTPS_ERRORS',
                                               PUPPETEER_IGNORE_HTTPS_ERRORS)
        cls.slow_mo = settings.get('PUPPETEER_SLOW_MO', PUPPETEER_SLOW_MO)
        cls.ignore_default_args = settings.get('PUPPETEER_IGNORE_DEFAULT_ARGS',
                                               PUPPETEER_IGNORE_DEFAULT_ARGS)
        cls.handle_sigint = settings.get('PUPPETEER_HANDLE_SIGINT', PUPPETEER_HANDLE_SIGINT)
        cls.handle_sigterm = settings.get('PUPPETEER_HANDLE_SIGTERM', PUPPETEER_HANDLE_SIGTERM)
        cls.handle_sighup = settings.get('PUPPETEER_HANDLE_SIGHUP', PUPPETEER_HANDLE_SIGHUP)
        cls.auto_close = settings.get('PUPPETEER_AUTO_CLOSE', PUPPETEER_AUTO_CLOSE)
        cls.devtools = settings.get('PUPPETEER_DEVTOOLS', PUPPETEER_DEVTOOLS)
        cls.executable_path = settings.get('PUPPETEER_EXECUTABLE_PATH', PUPPETEER_EXECUTABLE_PATH)
        cls.disable_extensions = settings.get('PUPPETEER_DISABLE_EXTENSIONS',
                                              PUPPETEER_DISABLE_EXTENSIONS)
        cls.hide_scrollbars = settings.get('PUPPETEER_HIDE_SCROLLBARS', PUPPETEER_HIDE_SCROLLBARS)
        cls.mute_audio = settings.get('PUPPETEER_MUTE_AUDIO', PUPPETEER_MUTE_AUDIO)
        cls.no_sandbox = settings.get('PUPPETEER_NO_SANDBOX', PUPPETEER_NO_SANDBOX)
        cls.disable_setuid_sandbox = settings.get('PUPPETEER_DISABLE_SETUID_SANDBOX',
                                                  PUPPETEER_DISABLE_SETUID_SANDBOX)
        cls.disable_gpu = settings.get('PUPPETEER_DISABLE_GPU', PUPPETEER_DISABLE_GPU)
        cls.download_timeout = settings.get('PUPPETEER_DOWNLOAD_TIMEOUT',
                                            settings.get('DOWNLOAD_TIMEOUT', PUPPETEER_DOWNLOAD_TIMEOUT))
        cls.ignore_resource_types = settings.get('PUPPETEER_IGNORE_RESOURCE_TYPES',
                                                 PUPPETEER_IGNORE_RESOURCE_TYPES)
        cls.screenshot = settings.get('PUPPETEER_SCREENSHOT', PUPPETEER_SCREENSHOT)
        cls.pretend = settings.get('PUPPETEER_PRETEND', PUPPETEER_PRETEND)
        cls.sleep = settings.get('PUPPETEER_SLEEP', PUPPETEER_SLEEP)
        cls.enable_request_interception = settings.get('ENABLE_REQUEST_INTERCEPTION',
                                                       ENABLE_REQUEST_INTERCEPTION)
        cls.retry_enabled = settings.get('RETRY_ENABLED')
        cls.max_retry_times = settings.get('RETRY_TIMES')
        cls.retry_http_codes = set(int(x) for x in setting.RETRY_HTTP_CODES)
        cls.priority_adjust = settings.get('RETRY_PRIORITY_ADJUST')
        cls.user_dir = settings.get('PUPPETEER_USER_DIR', PUPPETEER_USER_DIR)
        options = {
            'headless': cls.headless,
            'userDataDir': cls.user_dir,
            'dumpio': cls.dumpio,
            'devtools': cls.devtools,
            'args': [
                f'--window-size={cls.window_width},{cls.window_height}',
            ]
        }
        if cls.pretend:
            options['ignoreDefaultArgs'] = [
                '--enable-automation'
            ]
        if cls.executable_path:
            options['executablePath'] = cls.executable_path
        if cls.ignore_https_errors:
            options['ignoreHTTPSErrors'] = cls.ignore_https_errors
        if cls.slow_mo:
            options['slowMo'] = cls.slow_mo
        if cls.ignore_default_args:
            options['ignoreDefaultArgs'] = cls.ignore_default_args
        if cls.handle_sigint:
            options['handleSIGINT'] = cls.handle_sigint
        if cls.handle_sigterm:
            options['handleSIGTERM'] = cls.handle_sigterm
        if cls.handle_sighup:
            options['handleSIGHUP'] = cls.handle_sighup
        if cls.auto_close:
            options['autoClose'] = cls.auto_close
        if cls.disable_extensions:
            options['args'].append('--disable-extensions')
        if cls.hide_scrollbars:
            options['args'].append('--hide-scrollbars')
        if cls.mute_audio:
            options['args'].append('--mute-audio')
        if cls.no_sandbox:
            options['args'].append('--no-sandbox')
        if cls.disable_setuid_sandbox:
            options['args'].append('--disable-setuid-sandbox')
        if cls.disable_gpu:
            options['args'].append('--disable-gpu')
        cls.options = options
        # return cls.open_spider(spider)
        return cls(spider, **kwargs)

    async def getBrowser(self, options=None):
        self.logger.debug('Browser Render Opening...')
        self.browser = await launch(options or self.options)
        self.BROWSER_OPENED = True
        self.logger.debug('Browser Render Open Success.')

    async def _close_browser(self):
        await self.browser.close()

    async def check_browser_status(self):
        if self.BROWSER_OPENED is not True:
            return False
        return True

    async def process_request(self, request):
        if isinstance(request, PuppeteerRequest) is False:
            return request
        # if self.BROWSER_OPENED is None:
        #     self.BROWSER_OPENED = False
        #     await self.getBrowser()
        # elif self.BROWSER_OPENED is not True:  # 不确定是打开状态时先sleep一下
        #     await asyncio.sleep(2)
        # get puppeteer meta
        puppeteer_meta = request.meta.get('puppeteer') or {}
        self.logger.debug('Puppeteer_meta: %s', puppeteer_meta)
        if not isinstance(puppeteer_meta, dict) or len(puppeteer_meta.keys()) == 0:
            return

        page = await self.browser.newPage()

        await page.setViewport({'width': self.window_width, 'height': self.window_height})

        # set cookies
        parse_result = urlsplit(request.url)
        domain = parse_result.hostname
        _cookies = []
        if isinstance(request.cookies, dict):
            _cookies = [{'name': k, 'value': v, 'domain': domain}
                        for k, v in request.cookies.items()]
        else:
            for _cookie in _cookies:
                if isinstance(_cookie, dict) and 'domain' not in _cookie.keys():
                    _cookie['domain'] = domain
        await page.setCookie(*_cookies)

        _timeout = self.download_timeout
        if puppeteer_meta.get('timeout') is not None:
            _timeout = puppeteer_meta.get('timeout')

        self.logger.debug('Crawling %s', request.url)

        _response = None
        try:
            options = {
                'timeout': 1000 * _timeout
            }
            if puppeteer_meta.get('wait_until'):
                options['waitUntil'] = puppeteer_meta.get('wait_until')
            _response = await page.goto(
                request.url,
                options=options
            )
        except (errors.PageError, errors.TimeoutError):
            # logger.error('error rendering url %s using puppeteer', request.url)
            await page.close()
            # await self.browser.close()
            # return cls._retry(request, 504, spider)

            # wait for dom loaded
        if puppeteer_meta.get('wait_for'):
            _wait_for = puppeteer_meta.get('wait_for')
            try:
                self.logger.debug('Waiting For %s', _wait_for)
                if isinstance(_wait_for, dict):
                    await page.waitFor(**_wait_for)
                else:
                    await page.waitFor(_wait_for)
            except TimeoutError:
                self.logger.error('Error waiting for %s of %s', _wait_for, request.url)
                await page.close()
                # await self.browser.close()
                # return cls._retry(request, 504, spider)

        # evaluate script
        if puppeteer_meta.get('script'):
            _script = puppeteer_meta.get('script', 'navigator.webdriver')
            self.logger.debug('Evaluating %s', _script)
            await page.evaluate(_script)

        # sleep
        _sleep = self.sleep
        if puppeteer_meta.get('sleep') is not None:
            _sleep = puppeteer_meta.get('sleep')
        if _sleep is not None:
            self.logger.debug('Sleep for %ss', _sleep)
            await asyncio.sleep(_sleep)
        # print(await page.content())

        _text = ''
        try:
            _text = await page.content()
        except errors.NetworkError as ne:
            self.logger.warning('get content error: %s' % ne, exc_info=True)
            request.retry_times += 1
            return request
        finally:
            await page.close()
        try:
            _cookies = await page.cookies()
        except errors.NetworkError as ne:
            self.logger.warning('get cookies error: %s' % ne, exc_info=True)
        finally:
            await page.close()

        if not _response:
            self.logger.warning('Get null response by puppeteer of url %s', request.url)
            request.retry_times += 1
            return request

        _response.headers.pop('content-encoding', None)
        _response.headers.pop('Content-Encoding', None)

        response = PuppeteerResponse(
            url=page.url,
            status=_response.status,
            headers=_response.headers,
            cookies=_cookies,
            # content=bytes(text, encoding='utf-8'),
            text=_text,
            request=request
        )
        # if screenshot:
        #     response.meta['screenshot'] = screenshot
        await page.close()
        """
        print(page.isClosed())
        # print(self.browser.process.pid)
        pages = await self.browser.pages()
        for p in pages:
            print(p.url)
        if len(pages) <= 1 and pages[0].url == 'about:blank':
            await self.browser.close()
        # tasks = asyncio.all_tasks()
        # for task in tasks:
        #     print(task)
        """
        return response
