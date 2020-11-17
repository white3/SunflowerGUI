#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 12:43
# @Author  : Menzel3
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @version : 0.0.1
from PyQt5 import QtGui, QtWidgets
import ctypes, sys

from sunflower.internal.window import Window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    try:
        # 加载 UI设计
        gui = Window()
        gui.setupUi(MainWindow)

        # 加载 标题
        MainWindow.setWindowTitle('UCAS 4.5M Telescope')

        # 防止windows下加载 图标失败
        sys.platform.index('win')
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        # 加载 图标
        MainWindow.setWindowIcon(QtGui.QIcon('res/favicon.ico'))

        # 加载控制器
        gui.setupSunflower()

        # 显示 GUI
        MainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e.with_traceback())