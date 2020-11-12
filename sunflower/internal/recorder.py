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

HA="HAOffsetTabel"
DEC="DECOffsetTabel"
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
            cursor = c.execute("SELECT ha, haOffset from " + HA + " where ha < ? and ha > ?", (scale[0], scale[1]))
        else:
            cursor = c.execute("SELECT dec, decOffset from " + DEC + " where dec < ? and dec > ?", (scale[0], scale[1]))
        angle, offsets = [], []
        for row in cursor:
            angle.append(row[0])
            offsets.append(row[1])
        return angle, offsets

    def writeData(self, haOffset: HAOffset, decOffset: DECOffset):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO HAOffsetTabel (ha,haOffset,localTime,version,target) VALUES (?, ?, ?, ?, ?)",
            (haOffset.ha, haOffset.haOffset, haOffset.localTime.toString(), haOffset.version, haOffset.target.__str__())
        )
        c.execute(
            "INSERT INTO DECOffsetTabel (dec,decOffset,localTime,version,target) VALUES (?,?,?,?,?)",
            (decOffset.dec, decOffset.decOffset, decOffset.localTime.toString(), haOffset.version, haOffset.target.__str__())
        )
        self.conn.commit()