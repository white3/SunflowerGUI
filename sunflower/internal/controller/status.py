#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/18 22:35
# @Author  : Menzel3
# @Site    : 
# @File    : status.py
# @Software: PyCharm
# @version : 0.0.1


import functools
import pprint

from PyQt5.QtCore import QDateTime
from sunflower.internal.constants import constant

setup_display = False
statusTextBrowser = None


def display_status(status: str, color=constant.LOW):
    """
    LOW = "#000000"
    MEDIUM = "#00aaff"
    HIGH = "#00aaff"
    :param color: 配置状态信息的颜色
    :param status: 需要显示的状态信息
    :return:
    """
    log = "<font color=\"%s\">[+]%d %s</font>" % (color, QDateTime.currentDateTime().toTime_t(), status.__str__())
    statusTextBrowser.append(log)


def status_log(status, color=constant.LOW):
    def execute(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if setup_display:
                    display_status(status, color)
                print("function: %s" % (func.__name__))
                pprint.pprint(args)
                pprint.pprint(kwargs)
                return func(*args, **kwargs)
            except Exception as e:
                if setup_display:
                    print(e)
                    display_status(e, color)
                print(e)

        return wrapper

    return execute
