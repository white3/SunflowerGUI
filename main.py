#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 12:43
# @Author  : Menzel3
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @version : 0.0.1
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
import ctypes, sys

from sunflower import config, window, control

try:
    sys.platform.index('win')
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
except Exception as e:
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    # ui = mainWindow.Ui_DebugTerminalForm()
    # ui = mainWindow.Ui_DebugGUIForm()

    config = config.config()
    try:
        sunFlower = control.control(config=config)
        ui = window.window()
        MainWindow.setWindowTitle('UCAS 4.5M Telescope')
        MainWindow.setWindowIcon(QIcon('sunflower/favicon.ico'))
        ui.setupUi(MainWindow)
        ui.setupAction(MainWindow, sunFlower)
        MainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e.with_traceback())
        config.saveConfig()