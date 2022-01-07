# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 9:32
# @Author  : ZhaoXiangPeng
# @File    : setting_loader.py

import os
from .misc import load_settings
from configparser import ConfigParser, NoSectionError
# from ..settings import SETTING_LIST, DEFAULT_PUPPETEER_SETTINGS


class SettingLoader:
    settings = {}

    @classmethod
    def from_crawler(cls, _SETTING_: list = None, spider=None):
        """
        从启动路径找到所有的配置
        :return:
        """
        # 启动路径
        WORKING_DIRECTORY = os.getcwd()  # '..'  #
        # 项目绝对路径
        PROJECT_ABSOLUTE_PATH = os.path.dirname(os.path.abspath(WORKING_DIRECTORY))
        # print('-'*50+'\n', PROJECT_ABSOLUTE_PATH, '\n'+'-'*50)
        # 资源根路径
        _slash = PROJECT_ABSOLUTE_PATH.replace('\\', '/').rindex('/')
        SOURCE_ROOT = PROJECT_ABSOLUTE_PATH[_slash + 1:]
        # 基础配置
        setting_list = SETTING_LIST
        if _SETTING_:
            setting_list = _SETTING_

        # 1. 在项目中找自定义配置文件
        custom_setting = {}
        custom_setting_file = f'{PROJECT_ABSOLUTE_PATH}/ReSpider.ini'
        cfg_parse = ConfigParser()
        try:
            cfg_parse.read(custom_setting_file)
            custom_setting_path = cfg_parse.get('settings', 'default')
        except NoSectionError:
            pass
        else:
            custom_setting = load_settings(custom_setting_path)

        # 2. 判断 PUPPETEER 是否在自定义配置中(加载自定义的中间件)
        if 'ReSpider.extend.puppeteer.downloadmiddleware.PuppeteerMiddleware' in custom_setting.get('DOWNLOADER_MIDDLEWARES', {}):
            setting_list.append(DEFAULT_PUPPETEER_SETTINGS)

        # 3. 加载所有配置
        for setting in setting_list:
            cls.settings.update(load_settings(setting))

        # 4. 更新项目相关配置
        cls.settings.update(WORKING_DIRECTORY=WORKING_DIRECTORY,
                            PROJECT_ABSOLUTE_PATH=PROJECT_ABSOLUTE_PATH,
                            SOURCE_ROOT=SOURCE_ROOT,
                            LOG_FILE_DIRECTORY=f'{PROJECT_ABSOLUTE_PATH}/log/',
                            DATA_FILE_DIRECTORY=f'{PROJECT_ABSOLUTE_PATH}/data/')
        cls.settings.update(custom_setting)

        # Todo 所有配置加载完成后加载
        # 5. 加载配置所需文件
        cls.open_spider()
        return cls.settings

    @classmethod
    def open_spider(cls):
        """
        加载配置
        :return:
        """
        for k in ['LOG_FILE_DIRECTORY', 'DATA_FILE_DIRECTORY']:
            dir_ = cls.settings.get(k, '')
            if not os.path.exists(dir_):
                os.mkdir(dir_)
