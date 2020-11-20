#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/18 9:45
# @Author  : Menzel3
# @Site    : 
# @File    : circle_lock.py
# @Software: PyCharm
# @version : 0.0.1
import threading


class CircleLock(object):
    _lock = threading.Condition()
    _waiting_writers = 0
    _readers = 0
    _writing_writers = 0
    _prefer_writer = True

    def read_lock(self):
        """
        读者加锁
        :return:
        """
        with self._lock:
            while self._writing_writers > 0 or self._prefer_writer and self._waiting_writers > 0:
                self._lock.wait()
            self._readers += 1

    def read_unlock(self):
        """
        读者放锁
        :return:
        """
        with self._lock:
            self._readers -= 1
            self._prefer_writer = True
            self._lock.notifyAll()

    def write_lock(self):
        """
        写着加锁
        :return:
        """
        with self._lock:
            self._waiting_writers += 1
            try:
                while self._writing_writers > 0 or self._prefer_writer and self._waiting_writers > 0:
                    self._lock.wait()
                self._writing_writers += 1
            finally:
                self._waiting_writers -= 1

    def write_unlock(self):
        """
        写者放锁
        :return:
        """
        with self._lock:
            self._prefer_writer = False
            self._writing_writers -= 1
            self._lock.notifyAll()
