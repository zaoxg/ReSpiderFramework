# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 16:02
# @Author  : ZhaoXiangPeng
# @File    : create_builder.py

from .create import CreateSpider, CreateProject
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
        help="创建爬虫 如 ReSpider create -s <spider_name>",
    )

    args = create.parse_args()
    if args.spider:
        spider_name, *spider_type = args.spider
        CreateSpider().create(spider_name, spider_type)
    elif args.project:
        CreateProject().create(args.project)

