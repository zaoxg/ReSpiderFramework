# -*- coding: utf-8 -*-
# @Time    : 2022/2/14 13:51
# @Author  : ZhaoXiangPeng
# @File    : dingtalk.py
# @Document: https://open.dingtalk.com/document/group/custom-robot-access

import enum
import json
import asyncio
import datetime
import requests
import ReSpider.setting as setting
from ReSpider.http.request import Request
api = 'https://oapi.dingtalk.com/robot/send?access_token=41c3e45e6080d296d3e0b987f0aacd2827797c94de045f471522410be62a3aad'


class MessageType:
    TEXT = 'text'  # 文本
    LINK = 'link'  # 链接
    MARKDOWN = 'markdown'  # markdown
    ACTION_CARD = 'ActionCard'  # ActionCard
    FEED_CARD = 'FeedCard'  # FeedCard


class DingTalkNotify:
    def __init__(
        self,
        webhook: str = None,
        secret: str = None,
        fail_notice: bool = False  # 通知失败通知
    ):
        """
        机器人初始化
        :param webhook: 钉钉群自定义机器人webhook地址
        :param secret: 机器人安全设置页面勾选“加签”时需要传入的密钥
        :param fail_notice: 消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结果自行判断和处理
        """
        self.webhook = webhook or setting.DINGTALK_WEBHOOK
        self.secret = secret
        self.fail_notice = fail_notice

    def notify(self, data):
        req = Request(
            url=self.webhook,
            method='POST',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data, ensure_ascii=False)
        )
        loop = asyncio.get_event_loop()
        loop.create_task(req())

    def send_text(self, msg: str,
                  is_at_all=False, at_mobiles: list = None,
                  at_dingtalk_ids: list = None,
                  is_auto_at=True):
        data = {'msgtype': 'text', 'at': {}}
        if not msg:
            raise ValueError('消息内容不能为空')
        data['text'] = {'content': msg}

        if is_at_all:
            data['at']['isAtAll'] = is_at_all
        if at_mobiles:
            data['at']['atMobiles'] = at_mobiles
        return self.notify(data)


if __name__ == '__main__':
    # python 3.8
    import time
    import hmac
    import hashlib
    import base64
    import urllib.parse

    timestamp = str(round(time.time() * 1000))
    secret = 'this is secret'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print(timestamp)
    print(sign)
    msg = "这个即将发布的新版本，创始人xx称它为红树林。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是红树林"
    DingTalkNotify().send_text(msg)
