#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/18 15:23
# @Author  : Menzel3
# @Site    : 
# @File    : container.py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.model.circle_lock import CircleLock
from copy import copy, deepcopy
from sunflower.internal.model.circle_lock import CircleLock
from threading import Lock

class ConcurrentMeta(object):
    def __init__(self):
        self.condition = CircleLock()


class ConDataContainer(object):
    def __init__(self):
        self.__data = {}
        self.__lock = {}

    # def exec(self, key, func, *args, **kw):
    #     if self.lock.get(key) is None:
    #         raise Exception('未初始%s变量' % key)
    #     self.lock[key].write_lock()
    #     func(self.data[key], *args, **kw)
    #     self.lock[key].write_unlock()

    def unsafe_set(self, key, value):
        if self.__lock.get(key) is None:
            self.__lock[key] = Lock()
        self.__data[key] = value

    def get_lock(self, key):
        if self.__lock.get(key) is None:
            return None
        return self.__lock[key]

    def set(self, key, value, timeout=-1, blocking=True):
        if self.__lock.get(key) is None:
            self.__lock[key] = Lock()
        self.__lock[key].acquire(timeout=timeout, blocking=blocking)
        self.__data[key] = value
        self.__lock[key].release()

    def get(self, key, lock=False):
        if self.__lock.get(key) is None:
            return None, None
        if lock:
            return self.__data[key], self.get_lock(key)
        else:
            return self.__data[key]


class ConcurrentDataContainer(dict):
    """
    用作共享对象包装器
    """
    locks = {}

    def __init__(self, *args, **kwargs):
        super(ConcurrentDataContainer, self).__init__(*args, **kwargs)

    def __getattribute__(self, item):
        """
        object.item, 如果报错则调用 __getattr__
        :param item:
        :return:
        """
        # try:
        # self['locks'][item].read_lock()
        return super().__getattribute__(item)
        # finally:
        # self['locks'][item].read_unlock()

    def __getitem__(self, item):
        # try:
        # self['locks'][item].read_lock()
        return super().__getitem__(item)
        # finally:
        # self['locks'][item].read_unlock()

    def __setattr__(self, key, value):
        # if not self['locks'][key]:
        # self['locks'][key] = CircleLock()
        # self['locks'][key].write_lock()
        self[key] = value
        # self['locks'][key].write_unlock()
        # try:
        # finally:
        #     self['locks'][key].write_unlock()

    def __getattr__(self, name):
        value = self[name]
        if isinstance(value, dict):
            # self.locks[name] = CircleLock()
            value = ConcurrentDataContainer(value)
        return value

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
