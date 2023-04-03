# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 10:29
# @Author  : ZhaoXiangPeng
# @File    : client.py

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('ja3er.com', 443))
host = socket.gethostname()
port = 12345

s.connect((host, port))
print(s.recv(1024))
s.close()
