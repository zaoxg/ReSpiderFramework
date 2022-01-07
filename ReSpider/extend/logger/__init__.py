# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:47
# @Author  : ZhaoXiangPeng
# @File    : __init__.py.py

import os
import logging
import ReSpider.setting as setting


class LogMixin:
    def __init__(self, spider=None, **kwargs):
        self.logger = self.get_logger(spider)

    def get_logger(self,
                   spider=None,
                   name=None,
                   log_mode=None,
                   encoding=None,
                   log_path=None,
                   log_level_console=None, log_level_file=None):
        # _setting = spider.settings
        log_file_name = spider.name or spider.__class__.name or spider.__class__.__name__
        name = '.'.join([self.__module__, name or self.__class__.__name__])

        # 实例化时先传入位置和名字
        logger = logging.getLogger(name)
        logger.setLevel(level=logging.DEBUG)

        # Formatter
        formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] [line:%(lineno)d] %(message)s",
                                      datefmt='%Y-%m-%d %H:%M:%S')

        # FileHandler
        if setting.LOG_TO_FILE is True:
            log_file_path = log_path or setting.LOG_PATH
            if not os.path.exists(log_file_path):
                os.mkdir(log_file_path)
            file_level = log_level_file or setting.LOG_LEVEL_FILE
            log_mode = log_mode or setting.LOG_MODE
            encoding = encoding or setting.LOG_ENCODING
            file_handler = logging.FileHandler(f'{log_file_path}/{log_file_name}.log',
                                               mode=log_mode if file_level == 'DEBUG' else 'a', encoding=encoding)
            file_handler.setLevel(file_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # StreamHandler
        if setting.LOG_TO_CONSOLE is True:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(log_level_console or setting.LOG_LEVEL_CONSOLE)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        return logger
