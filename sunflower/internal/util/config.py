#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:15
# @Author  : Menzel3
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @version : 0.0.1

import configparser
from sunflower.internal.util.decorator import debugLog


class Config:
    def __init__(self, configFilePath="config.ini"):
        '''
        修改配置并关闭程序后会自动保存至文件

        :param configFilePath: 配置文件路径
        '''
        # change 标记配置是否被修改
        self.isChange = False
        self.configFilePath = configFilePath
        self.config = configparser.ConfigParser()
        self.config.read(configFilePath)

    @debugLog
    def getValue(self, section, option):
        '''
        获取配置中属性名 key 对应的键值.

        :param key: 配置文件的属性名
        :return:
        '''
        return self.config.get(section=section, option=option)

    @debugLog
    def setValue(self, section, option, value):
        '''
        将配置中属性名 key 对应的键值修改为 value.

        :param key: 属性名称
        :param value: 属性值
        :return:
        '''
        self.config.set(section=section, option=option, value=value)

    def checkConfig(self, filePath):
        # TODO make config check.
        return True
