# -*- coding: utf-8 -*-
# @Time    : 2022/2/23 15:55
# @Author  : ZhaoXiangPeng
# @File    : cmdline.py

import sys
from os.path import dirname, join
from . import create_builder


def _print_commands():
    """
    @summery: copy form https://github.com/Boris-code/feapder/blob/master/feapder/commands/cmdline.py
    """
    with open(join(dirname(dirname(__file__)), "VERSION"), "rb") as f:
        version = f.read().decode("ascii").strip()

    print("ReSpider {}".format(version))
    print("\nUsage:")
    print("  ReSpider <command> [options] [args]\n")
    print("Available commands:")
    cmds = {
        "create": "create project、spider、setting",
        # "shell": "debug response",
        # "zip": "zip project",
    }
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass))

    print('\nUse "ReSpider <command> -h" to see more info about a command')


def execute():
    args = sys.argv
    if len(args) < 2:
        _print_commands()
        return

    command = args.pop(1)
    if command == "create":
        create_builder.main()
    # elif command == "shell":
    #     shell.main()
    # elif command == "zip":
    #     zip.main()
    else:
        _print_commands()


if __name__ == '__main__':
    execute()
