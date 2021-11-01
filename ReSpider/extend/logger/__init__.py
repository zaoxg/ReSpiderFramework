# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:47
# @Author  : ZhaoXiangPeng
# @File    : __init__.py.py

import logging
from .settings import STREAM_HANDLER_LEVEL, FILE_HANDLER_LEVEL


class LogMixin:
    def __init__(self, spider=None):
        self.logger = self.get_logger(spider)

    def get_logger(self, spider, name=None):
        _setting = spider.settings
        log_files_path = _setting.get('LOG_FILE_DIRECTORY', '../')
        log_file_name = spider.name or spider.__class__.name or spider.__class__.__name__
        name = '.'.join([self.__module__, name or self.__class__.__name__])

        # 实例化时先传入位置和名字
        logger = logging.getLogger(name)
        logger.setLevel(level=logging.DEBUG)

        # Formatter
        formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] [line:%(lineno)d] %(message)s",
                                      datefmt='%Y-%m-%d %H:%M:%S')

        # FileHandler
        file_level = _setting.get('FILE_HANDLER_LEVEL', FILE_HANDLER_LEVEL)
        file_handler = logging.FileHandler(f'{log_files_path}/{log_file_name}.log',
                                           mode='w' if file_level == 'DEBUG' else 'a', encoding="utf-8")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # StreamHandler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(_setting.get('STREAM_HANDLER_LEVEL', STREAM_HANDLER_LEVEL))
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger
