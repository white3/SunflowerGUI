#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/22 21:16
# @Author  : Menzel3
# @Site    : 
# @File    : test.py
# @Software: PyCharm
# @version : 0.0.1
from pprint import *
import threading

class printImp:
    def __init__(self, name, message):
        self.name = name
        self.message = message

    def print(self):
        pprint(self.message)

class print:
    def __init__(self):
        self.printImp = printImp('mz3', 'test123')
        self.printThread = threading.Thread(target=self.printImp.print, daemon=True)
        self.printLock = threading.Condition()
        self.isPrint = True

    def doPrint(self):
        while True:
            if not self.isPrint:
                self.printLock.acquire()
            self.printImp.print()
        # self.printLock.acquire()
        #
        # self.printLock.release()

    def start(self):
        self.printThread.start()

    def stop(self):
        self.printThread._tstate_lock

