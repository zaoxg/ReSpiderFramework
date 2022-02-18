# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:47
# @Author  : ZhaoXiangPeng
# @File    : __init__.py.py

import os
import logging
import ReSpider.setting as setting


class LogMixin:
    logger = None

    def __init__(self, spider=None, **kwargs):
        if self.logger is None:
            self.logger = self.get_logger(spider)

    # def __getattr__(self, name):
    #     # 调用log时再初始化，为了加载最新的setting
    #     if self.__class__.logger is None:
    #         self.__class__.logger = self.get_logger()
    #     return getattr(self.__class__.logger, name)

    def get_logger(self,
                   spider=None,
                   log_name=None,
                   log_mode=None,
                   encoding=None,
                   log_path=None,
                   log_level_console=None, log_level_file=None):
        # _setting = spider.settings
        module_group = self.__module__.split('.')
        if module_group[0] != module_group[-1]:
            self.__module__ = module_group[0]+'.'+module_group[-1]
        name = '.'.join([self.__module__, self.__class__.__name__])

        # 实例化时先传入位置和名字
        logger = logging.getLogger(name)
        logger.setLevel(level=logging.DEBUG)

        # Formatter
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | line:%(lineno)d | %(message)s",
                                      datefmt='%Y-%m-%d %H:%M:%S')
        # FileHandler
        if setting.LOG_TO_FILE is True:
            log_file_path = log_path or setting.LOG_PATH
            if not os.path.exists(log_file_path):
                os.mkdir(log_file_path)
            log_file_name = log_name or setting.LOG_NAME
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


class Logger:
    log = None

    def __getattr__(self, name):
        # 调用log时再初始化，为了加载最新的setting
        if self.__class__.log is None:
            self.__class__.log = get_logger()
        return getattr(self.__class__.log, name)

    @property
    def debug(self):
        return self.__class__.log.debug

    @property
    def info(self):
        return self.__class__.log.info

    @property
    def warning(self):
        return self.__class__.log.warning

    @property
    def exception(self):
        return self.__class__.log.exception

    @property
    def error(self):
        return self.__class__.log.error

    @property
    def critical(self):
        return self.__class__.log.critical
