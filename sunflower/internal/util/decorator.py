#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 19:03
# @Author  : Menzel3
# @Site    : 
# @File    : decorator.py
# @Software: PyCharm
# @version : 0.0.1


def debugLog(func):
    def wrapper(*args, **kw):
        try:
            print("%s(%s) is running" % (func.__name__, kw))
            return func(*args, **kw)
        except Exception as e:
            print(e)

    return wrapper
