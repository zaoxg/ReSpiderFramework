# -*- coding: utf-8 -*-
# @Time    : 2022/2/14 13:51
# @Author  : ZhaoXiangPeng
# @File    : dingtalk.py

import json
import requests
api = 'https://oapi.dingtalk.com/robot/send?access_token=41c3e45e6080d296d3e0b987f0aacd2827797c94de045f471522410be62a3aad'


class Message:
    msgtype: str = 'text'
    text: dict = None
    at: dict = None


class DingTalkNotify:
    def notify(self, content=None, slot=None):
        msg_content = {
            "msgtype": "text",
            "text": {
                "content": "NotifyTest: 我就是我, 是不一样的烟火"
            }
        }
        resp = requests.post(
            url=api,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'ReSpiderNotify/1.0-Beta'
            },
            data=json.dumps(msg_content, ensure_ascii=False)
        )
