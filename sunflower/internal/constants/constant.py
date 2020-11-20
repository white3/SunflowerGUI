#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 20:06
# @Author  : Menzel3
# @Site    : 
# @File    : py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.util.config import Config
from sunflower.internal.util.sqlite_utils import SqliteUtils
import pytz

# 配置文件管理模块
config = Config()
sql_util = SqliteUtils()

# color
LOW = "#000000"
MEDIUM = "#00aaff"
HIGH = "#ff0000"

SPEED_MAX = 3600    # 1°

# flush time
VIEW_FLUSH_TIME = float(config.getValue(section="view", option="FLUSH_TIME"))
TRACE_FLUSH_TIME = float(config.getValue(section="trace", option='FLUSH_TIME'))
RECORD_FLUSH_TIME = float(config.getValue(section="record", option="FLUSH_TIME"))
CORRECT_FLUSH_TIME = float(config.getValue(section="correct", option="FLUSH_TIME"))

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
LOCAL_TIMEZONE = pytz.timezone(TIMEZONE)
UTC_TIMEZONE = pytz.UTC