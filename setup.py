# -*- coding: utf-8 -*-
# @Time    : 2022/2/18 14:48
# @Author  : ZhaoXiangPeng
# @File    : setup.py
"""
发布流程
py -m pip install twine  # 您将需要它来将您的项目分发上传到PyPI
# 打包为 whl文件
py -m build --wheel
# 检查
twine check dist/*
# 更新/发布
twine upload --repository testpypi dist/*  # 测试 zhaoxiangpeng
twine upload dist/*
"""

from os.path import dirname, join
from sys import version_info
import setuptools

if version_info < (3, 8, 0):
    raise SystemExit("Sorry! ReSpider requires python 3.8.0 or later.")

with open(join(dirname(__file__), "ReSpider/VERSION"), "rb") as f:
    version = f.read().decode("ascii").strip()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = setuptools.find_packages(
    exclude=["TestProject", "TestProject.*",
             "tests", "tests.*"]
)
packages.extend([
    "ReSpider",
    "ReSpider.templates",
    "ReSpider.templates.project_template",
    "ReSpider.templates.project_template.spiders"
])

requires = [
    "urllib3>=1.25.8",
    "requests>=2.22.0",
    "aiohttp>=3.7.3",
    "cchardet>=2.1.7",
    "parsel>=1.6.0",
    "aiofiles>=0.6.0",
    "aiocsv>=1.2.1",
    "redis>=2.10.6,<4.0.0",
    "pymongo>=3.11.2",
    "motor>=2.3.1",
    "pyppeteer>=0.2.5",
    "PyExecJS>=1.5.1"
]

setuptools.setup(
    name="ReSpider",
    version=version,
    author="zhaoxiangpeng",
    author_email="zhaoxiangpengSR@gmail.com",
    description="ReSpider 是一款 整合了实用工具的 python 爬虫程序",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhaoxplab/ReSpiderFramework",
    project_urls={
        "Bug Tracker": "https://github.com/zhaoxplab/ReSpiderFramework/issues",
    },
    keywords='aiohttp spider',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    include_package_data=True,
    packages=packages,
    python_requires=">=3.8",
    install_requires=requires,
    entry_points={"console_scripts": ["respider = ReSpider.extend.cmd.cmdline:execute", "ReSpider = ReSpider.extend.cmd.cmdline:execute"]}
)