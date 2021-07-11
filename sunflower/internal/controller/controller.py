#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 23:10
# @Author  : Menzel3
# @Site    :
# @File    : controller.py
# @Software: PyCharm
# @version : 0.0.1
from abc import ABC

from sunflower.internal.meta import interruptible_thread, singleton_meta


class SinController(metaclass=singleton_meta.SingletonMeta):
    pass


class Controller(object):

    def setup(self) -> bool:
        return False


class ConController(interruptible_thread.ThreadMeta, Controller, ABC):
    pass
