# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 16:17
# @Author  : ZhaoXiangPeng
# @File    : create_project.py

import getpass
import os
import shutil
import ReSpider.utils.tools as tools


def deal_file_info(file):
    file = file.replace("{DATE}", tools.get_current_date(date_format="%Y/%m/%d %H:%M"))
    file = file.replace("{USER}", getpass.getuser())

    return file


class CreateProject:

    def copy_callback(self, src, dst, *, follow_symlinks=True):
        if src.endswith(".py"):
            with open(src, "r", encoding="utf-8") as src_file, open(
                    dst, "w", encoding="utf8"
            ) as dst_file:
                content = src_file.read()
                content = deal_file_info(content)
                dst_file.write(content)

        else:
            shutil.copy2(src, dst, follow_symlinks=follow_symlinks)

    def create(self, project_name):
        if os.path.exists(project_name):
            print('%s 项目已经存在' % project_name)
        else:
            template_path = os.path.abspath(
                os.path.join(__file__, '../../../templates/project_template')
            )
            shutil.copytree(
                template_path, project_name, copy_function=self.copy_callback
            )
            print("\n%s 项目生成成功" % project_name)
