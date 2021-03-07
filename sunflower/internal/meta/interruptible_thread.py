#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 14:55
# @Author  : Menzel3
# @Site    : 
# @File    : interruptible_thread.py
# @Software: PyCharm
# @version : 0.0.1
import threading
from abc import abstractmethod


class ThreadMeta(object):

    def __del__(self):
        self.wait()
        self.exit()

    def __init__(self):
        self.__isRunning = threading.Condition()  # a global lock to Control the thread of working
        self.__flag = True  # True表示运行, False表示停止运行
        self.__isExiting = False  # False表示不退出，True 表示退出
        self.__workThread = threading.Thread(target=self.__working, daemon=True)
        self.__workThread.start()
        # time.sleep(1)

    def run(self):
        """
        如果原本就在运行，不会改变什么
        :return:
        """
        self.__flag = False
        try:
            self.__isRunning.acquire()
            self.__isRunning.notify()
        finally:
            self.__isRunning.release()

    def exit(self):
        """
        关闭并退出线程
        :return:
        """
        self.__flag = True
        self.__isExiting = True

    def status(self) -> bool:
        """

        :return: True 运行中; False 停止中
        """
        return not self.__flag

    def wait(self):
        """
        线程进入等待
        :return:
        """
        self.__flag = True

    def __working(self):
        while True:
            # if traceFlag is True, the doTrace thread will wait for notification
            if self.__flag:
                print("stop")
                if self.__isExiting:
                    print("exit")
                    break
                # 自我睡眠
                try:
                    self.__isRunning.acquire()
                    self.__isRunning.wait()
                finally:
                    self.__isRunning.release()
            self.before_work()
            self.work()
            self.after_work()

    def before_work(self):
        pass

    def after_work(self):
        pass

    @abstractmethod
    def work(self):
        pass
