#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/22 21:16
# @Author  : Menzel3
# @Site    : 
# @Software: PyCharm
# @version : 0.0.1
from pprint import *
import threading

class printImp:
    def __init__(self, name, message):
        self.name = name
        self.message = message

    def printt(self):
        pprint(self.message)

class aprint:
    def __init__(self):
        self.printImp = printImp('mz3', 'test123')
        self.printThread = threading.Thread(target=self.printImp.printt, daemon=True)
        self.printLock = threading.Condition()
        self.isPrint = True

    def statusLog(func):
        def wrapper(*args, **kwargs):
            print("%s is running" % func.__name__)
            print(args[0])
            return func(*args, **kwargs)
        return wrapper

    @statusLog
    def doPrint(self):
        while True:
            if not self.isPrint:
                self.printLock.acquire()
            self.printImp.printt()
        # self.printLock.acquire()
        #
        # self.printLock.release()

    @statusLog
    def start(self):
        self.printThread.start()

    @statusLog
    def stop(self):
        self.printThread._tstate_lock

if __name__ == '__main__':
    a = aprint()
    a.stop()