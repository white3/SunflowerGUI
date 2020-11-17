#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 19:03
# @Author  : Menzel3
# @Site    : 
# @File    : decorator.py
# @Software: PyCharm
# @version : 0.0.1

import functools


def debugLog(func):
    def wrapper(*args, **kw):
        print("%s(%s) is running" % (func.__name__, kw))
        return func(*args, **kw)
    return wrapper

def statusLog(object):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("%s is running" % func.__name__)
            object.displayStatus("%s is running" % func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def delayRun(waitTime):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print("%s is running" % func.__name__)
            # sleep(waitTime)
            return func(*args, **kw)
        return wrapper
    return decorator

