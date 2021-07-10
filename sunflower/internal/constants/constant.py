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

SPEED_MAX = 3600  # 1°

# flush time
limit = float(config.getValue(section='trace', option='limit'))
VIEW_FLUSH_TIME = float(config.getValue(section="view", option="FLUSH_TIME"))
TRACE_FLUSH_TIME = float(config.getValue(section="trace", option='FLUSH_TIME'))
RECORD_FLUSH_TIME = float(config.getValue(section="record", option="FLUSH_TIME"))
DETECT_FLUSH_TIME = float(config.getValue(section="serial", option="DETECT_FLUSH_TIME"))
SERIAL_FLUSH_TIME = float(config.getValue(section="serial", option="SERIAL_FLUSH_TIME"))
# serial
port = config.getValue(section='serial', option='port')
baudrate = int(config.getValue(section='serial', option='baudrate'))
timeout = float(config.getValue(section='serial', option='timeout'))

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

# is debug
is_debug = config.getValue(section='debug', option='status')

# light correct
CORRECT_FLUSH_TIME = float(config.getValue(section="correct", option="FLUSH_TIME"))
camera_width = float(config.getValue(section="correct", option="camera_width"))
camera_height = float(config.getValue(section="correct", option="camera_height"))
camera_center = [camera_width / 2, camera_height / 2]
camera_amplify_part = float(config.getValue(section="correct", option="camera_amplify_part"))
radius = int(config.getValue(section="correct", option="radius"))
camera_width_alpha = float(config.getValue(section="correct", option="camera_width_alpha"))
camera_height_alpha = float(config.getValue(section="correct", option="camera_height_alpha"))
camera_alpha_width_percentage = camera_width_alpha / camera_width
camera_alpha_height_percentage = camera_height_alpha / camera_height
