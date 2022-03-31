# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 16:02
# @Author  : ZhaoXiangPeng
# @File    : create_builder.py

from .create import *
import argparse


def main():
    create = argparse.ArgumentParser(description='创建')
    create.add_argument(
        '-p',
        '--project',
        help="创建项目 如 ReSpider create -p <project_name>",
        metavar=""
    )
    create.add_argument(
        '-s',
        '--spider',
        nargs='+',
        help="创建爬虫 如 ReSpider create -s <spider_name> <spider_type>"
        "spider_type=1 Spider;"
        "spider_type=2 RedisSpider;",
        metavar=""
    )
    create.add_argument(
        '--setting',
        help='创建全局配置文件' 'ReSpider create --setting',
        action="store_true"
    )

    args = create.parse_args()
    # print(args)
    if args.spider:
        spider_name, *spider_type = args.spider
        if not spider_type:
            spider_type = 1
        else:
            spider_type = spider_type[0]
        try:
            spider_type = int(spider_type)
        except:
            raise ValueError("spider_type error, support 1, 2, 3")
        CreateSpider().create(spider_name, spider_type)

    elif args.project:
        CreateProject().create(args.project)

    elif args.setting:
        CreateSetting().create()

