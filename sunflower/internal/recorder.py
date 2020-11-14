#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 0:46
# @Author  : Menzel3
# @Site    : 
# @File    : recorder.py
# @Software: PyCharm
# @version : 0.0.1
import sqlite3
from sunflower.internal.model.offset import HAOffset, DECOffset
from sunflower.internal.model.times import Times
from sunflower.internal.model.target import Target
import json

HA = "HAOffsetTabel"
DEC = "DECOffsetTabel"


# from sunflower.internal.util.sqliteUtils import SqliteUtils

class Recorder():
    def __init__(self):
        self.dbPath = './sunflower/internal/res/recorder.db'
        self.conn = sqlite3.connect(self.dbPath)

    # def readData(self, scale, earlyTime, lastTime):
    def readData(self, scale=[-180, 180], kind=HA) -> object:
        """
        :param scale: 筛选数据范围, 区间为[scale[0], scale[1]]
        :param kind: 标记取HA、还是DEC
        :return: 如果区间无数据将返回 -1
        """
        c = self.conn.cursor()
        if kind is HA:
            cursor = c.execute(
                "SELECT ha, haOffset, globalClock, version from HAOffsetTabel where ha > ? and ha < ? and version!=-2",
                (scale[0], scale[1]))
        else:
            cursor = c.execute(
                "SELECT dec, decOffset, globalClock, version from DECOffsetTabel where dec > ? and dec < ? and version!=-2",
                (scale[0], scale[1]))
        offset_packages = []
        for row in cursor:
            offset_packages.append([row[0], row[1], row[2], row[3]])
        return offset_packages

    def writeData(self, haOffset: HAOffset, decOffset: DECOffset, globalClock: Times, target: Target):
        """

        :param haOffset: 记录时角偏移量
        :param decOffset: 记录赤纬偏移量
        :param globalClock: 记录该偏移量对应的全局时钟
        :param target: 记录该偏移量对应的目标
        :return:
        """
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO HAOffsetTabel (ha,haOffset,globalClock,version,target) VALUES (?, ?, ?, ?, ?)",
            (haOffset.ha, haOffset.haOffset, json.dumps(globalClock), haOffset.version,
             json.dumps(target))
        )
        c.execute(
            "INSERT INTO DECOffsetTabel (dec,decOffset,globalClock,version,target) VALUES (?,?,?,?,?)",
            (decOffset.dec, decOffset.decOffset, json.dumps(globalClock), haOffset.version,
             json.dumps(target))
        )
        self.conn.commit()
