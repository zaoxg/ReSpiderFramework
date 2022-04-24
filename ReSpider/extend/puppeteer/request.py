# from ReSpider import Request
from ReSpider.http import Request
import copy


class PuppeteerRequest(Request):
    name = 'puppeteer request'

    def __init__(self, url, callback=None, wait_until=None, wait_for=None, script=None, proxy=None,
                 sleep=None, timeout=None, ignore_resource_types=None, pretend=None, screenshot=None, meta=None, *args,
                 **kwargs):
        meta = copy.deepcopy(meta) or {}
        puppeteer_meta = meta.get('puppeteer', {})

        self.wait_until = puppeteer_meta.get('wait_until', wait_until or 'domcontentloaded')
        self.wait_for = puppeteer_meta.get('wait_for', wait_for)
        self.script = puppeteer_meta.get('script', script)
        self.sleep = puppeteer_meta.get('sleep', sleep)
        self.proxy = puppeteer_meta.get('proxy', proxy)
        self.pretend = puppeteer_meta.get('pretend', pretend)
        self.timeout = puppeteer_meta.get('timeout', timeout)
        self.ignore_resource_types = puppeteer_meta.get('ignore_resource_types', ignore_resource_types)
        self.screenshot = puppeteer_meta.get('screenshot', screenshot)

        puppeteer_meta = meta.setdefault('puppeteer', {})
        puppeteer_meta['wait_until'] = self.wait_until
        puppeteer_meta['wait_for'] = self.wait_for
        puppeteer_meta['script'] = self.script
        puppeteer_meta['sleep'] = self.sleep
        puppeteer_meta['proxy'] = self.proxy
        puppeteer_meta['pretend'] = self.pretend
        puppeteer_meta['timeout'] = self.timeout
        puppeteer_meta['screenshot'] = self.screenshot
        puppeteer_meta['ignore_resource_types'] = self.ignore_resource_types

        super().__init__(url, callback=callback, meta=meta, *args, **kwargs)
