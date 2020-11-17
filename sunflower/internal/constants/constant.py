#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 20:06
# @Author  : Menzel3
# @Site    : 
# @File    : py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.util.config import Config
from sunflower.internal.util.sqliteUtils import SqliteUtils

# 配置文件管理模块
config = Config()
sql_util = SqliteUtils()

# color
LOW = "#000000"
MEDIUM = "#00aaff"
HIGH = "#ff0000"

SPEED_MAX = 3600    # 1°

# view
VIEW_FLUSH_TIME = float(config.getValue(section="view", option="FLUSH_TIME"))

# record
RECORD_FLUSH_TIME = float(config.getValue(section="record", option="FLUSH_TIME"))

# >>> ser = serial.Serial()
# >>> ser.baudrate = 19200
# >>> ser.port = 'COM1'
# >>> ser
# >>> ser.open()
# >>> ser.is_open
# >>> ser.close()
# >>> ser.is_open

# serial
port = config.getValue(section='serial', option='port')
baudrate = int(config.getValue(section='serial', option='baudrate'))

# offset
version = int(config.getValue(section='offset', option='version'))

# location
LAT = config.getValue(section='location', option='lat')
LON = config.getValue(section='location', option='lon')
ELEVATION = float(config.getValue(section='location', option='elevation'))

# time
TIMEZONE = config.getValue(section='time', option='timezone')