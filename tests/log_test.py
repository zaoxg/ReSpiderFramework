# -*- coding: utf-8 -*-
# @Time    : 2021/11/1 14:28
# @Author  : ZhaoXiangPeng
# @File    : log_test.py

import logging
import os
import ReSpider.setting as setting
LOG_FORMAT = "%(threadName)s|%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s| %(message)s"


def get_logger():
    # logger 配置
    name = os.path.basename(os.getcwd()).split(os.sep)[-1].split(".")[0]  # 取文件名

    _logger_ = logging.getLogger(name)
    _logger_.setLevel(level=logging.DEBUG)

    # Formatter
    # formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] [line:%(lineno)d] %(message)s",
    #                               datefmt='%Y-%m-%d %H:%M:%S')
    # Formatter
    formatter = logging.Formatter("%(threadName)s %(asctime)s %(filename)s %(funcName)s line:%(lineno)d %(levelname)s| %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')
    # FileHandler
    """
    file_level = _setting.get('FILE_HANDLER_LEVEL', FILE_HANDLER_LEVEL)
    file_handler = logging.FileHandler(f'{log_files_path}/{log_file_name}.log',
                                       mode='w' if file_level == 'DEBUG' else 'a', encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    _logger_.addHandler(file_handler)
    """
    # StreamHandler
    stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(_setting.get('STREAM_HANDLER_LEVEL', STREAM_HANDLER_LEVEL))
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    _logger_.addHandler(stream_handler)

    return _logger_


def get_log(
       obj=None,
       log_name=None,
       log_mode=None,
       encoding=None,
       log_path=None,
       log_level_console=None, log_level_file=None):
    # _setting = spider.settings
    name = '.'.join([obj.__module__, obj.__class__.__name__])

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
            self.__class__.log = get_log()
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


logger = Logger()
